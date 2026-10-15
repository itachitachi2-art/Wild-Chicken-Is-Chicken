"""Read-only metadata/CIL audit; does not load or execute any managed assembly."""
import sys, json, pathlib, struct, argparse
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--game-dll',required=True,type=pathlib.Path)
p.add_argument('--mod-dll',required=True,type=pathlib.Path)
p.add_argument('--output',required=True,type=pathlib.Path)
a=p.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from clrmeta import CLR
from cilscan import body, instructions

class CanonicalCLR(CLR):
    def typename(self, table, rid):
        if table == 1 and rid:
            row = self.rows[1][rid]
            scope_table, scope_rid = self.decode('ResolutionScope', row[0])
            if scope_table == 1:
                return self.typename(1, scope_rid) + '+' + self.string(row[1])
        return super().typename(table, rid)
    def root_type(self, table, rid):
        if table != 27:
            return table, rid
        d = self.blob(self.rows[27][rid][0]); pos = 0
        while d[pos] in (15, 16, 29, 69): pos += 1
        if d[pos] == 21: pos += 1
        if d[pos] not in (17, 18): raise ValueError('Non-named TypeSpec parent ' + d.hex())
        token, pos = self.uint(d, pos + 1)
        return self.decode('TypeDefOrRef', token)
    def type_assembly(self, table, rid):
        table, rid = self.root_type(table, rid)
        if table == 2: return self.identity()['assembly']
        if table != 1: return None
        st, sr = self.decode('ResolutionScope', self.rows[1][rid][0])
        while st == 1: st, sr = self.decode('ResolutionScope', self.rows[1][sr][0])
        return self.string(self.rows[35][sr][6]) if st == 35 else None

game = CanonicalCLR(str(a.game_dll))
mod = CanonicalCLR(str(a.mod_dll))
game_types = {game.typename(2, i): i for i in range(1, game.count.get(2, 0) + 1)}
refs = []; others = []
for idx, row in enumerate(mod.rows.get(10, [])[1:], 1):
    table, rid = mod.decode('MemberRefParent', row[0])
    if table not in (1, 2, 27):
        others.append({'token': hex(0x0a000000 | idx), 'reason': 'MemberRef parent is not a named type', 'table': table})
        continue
    assembly = mod.type_assembly(table, rid)
    if assembly != 'Assembly-CSharp': continue
    rt, rr = mod.root_type(table, rid)
    lookup_type = mod.typename(rt, rr)
    reference = {'token': hex(0x0a000000 | idx), 'parent': mod.typename(table, rid), 'lookup_type': lookup_type, 'name': mod.string(row[1]), 'signature': mod.signature(row[2]), 'kind': 'field' if mod.blob(row[2])[0] == 6 else 'method'}
    defid = game_types.get(lookup_type)
    members = []
    if defid:
        report = game.type_report(defid)
        members = report['fields' if reference['kind'] == 'field' else 'methods']
    reference['matches'] = [m for m in members if m['name'] == reference['name'] and m['signature'] == reference['signature']]
    reference['status'] = 'MATCH' if reference['matches'] else 'MISMATCH'
    if not reference['matches']:
        reference['same_name_candidates'] = [m for m in members if m['name'] == reference['name']]
    refs.append(reference)

critical = {'ItemInventoryData': {'holdingEntity', 'item', 'itemValue', 'itemStack', 'slotIdx', 'world', 'model'}, 'ItemValue': {'type', 'None'}, 'ItemStack': {'itemValue', 'count', 'Empty'}}
stale = [r for r in refs if r['kind'] == 'field' and r['lookup_type'] in critical and r['name'] in critical[r['lookup_type']]]
lookup = {int(r['token'], 16): r for r in refs}
calls = []; scan_errors = []; bodies_scanned = 0
for mid, m in enumerate(mod.rows.get(6, [])[1:], 1):
    if not m[0]: continue
    bodies_scanned += 1
    try:
        for offset, opcode, operand in instructions(body(mod, mid)):
            if opcode not in (0x28, 0x6f): continue
            target = lookup.get(struct.unpack('<I', operand)[0])
            if target and target['lookup_type'] in critical and target['name'].startswith(('get_', 'set_')):
                calls.append({'caller': mod.typename(2, mod.method_owner[mid]) + '.' + mod.string(m[3]), 'caller_token': hex(0x06000000 | mid), 'offset': hex(offset), 'opcode': 'call' if opcode == 0x28 else 'callvirt', 'target': target['lookup_type'] + '.' + target['name'], 'target_token': target['token']})
    except Exception as error:
        scan_errors.append({'method': hex(0x06000000 | mid), 'error': str(error)})
item = game.type_report(game_types['ItemInventoryData'])
summary = {'status': 'PASS' if all(r['status'] == 'MATCH' for r in refs) and not stale and not scan_errors and not others else 'REVIEW', 'scope': 'All MemberRef rows whose named root type resolves to Assembly-CSharp, including generic TypeSpec parents; exact member kind, canonical nested type names, and decoded signature comparison against supplied game metadata. Static CIL inspection only; no runtime game test.', 'member_refs_total': mod.count.get(10, 0), 'game_member_refs_checked': len(refs), 'mismatches': sum(r['status'] != 'MATCH' for r in refs), 'stale_critical_field_refs': len(stale), 'method_bodies_scanned': bodies_scanned, 'scan_errors': scan_errors, 'unclassified_member_refs': others, 'game_identity': game.identity(), 'mod_identity': mod.identity(), 'holdingEntity_game_fields': [f for f in item['fields'] if f['name'] == 'holdingEntity'], 'holdingEntity_game_properties': [p for p in item['properties'] if p['name'] == 'holdingEntity'], 'holdingEntity_game_accessors': [m for m in item['methods'] if m['name'] in ('get_holdingEntity', 'set_holdingEntity')], 'critical_getter_calls': calls, 'game_member_references': refs}
out = a.output
out.write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k:v for k,v in summary.items() if k != 'game_member_references'}, indent=2))
for r in refs:
    if r['status'] != 'MATCH': print('MISMATCH', json.dumps(r, indent=2))
print('Audit evidence:', out)
sys.exit(0 if summary['status'] == 'PASS' else 1)
