#!/usr/bin/env python3
"""Isolated ABI regression model. Never loads or executes actual game assemblies."""
from pathlib import Path
import json, subprocess, shutil, argparse
root = Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--mcs',default='mcs')
p.add_argument('--mono',default='mono')
p.add_argument('--source',type=Path,default=root.parents[1]/'WildChickenIsChicken/src/ItemActionWCICButcherChicken.cs')
a=p.parse_args(); source=a.source.resolve()

commands = []
def run(args, logfile=None):
    commands.append(list(map(str,args)))
    result = subprocess.run(list(map(str,args)), capture_output=True, text=True)
    output = result.stdout + result.stderr
    if logfile: logfile.write_text(output)
    if result.returncode: raise RuntimeError(output)
    return output
for variant in ('old-field', 'new-property'):
    out = root / variant; out.mkdir(exist_ok=True)
    args = [a.mcs,'/noconfig','/target:library','/out:'+str(out/'Assembly-CSharp.dll')]
    if variant == 'new-property': args += ['/define:PROPERTY_API']
    run(args + [root/'GameStub.cs'])
    run([a.mcs,'/noconfig','/target:library','/reference:'+str(out/'Assembly-CSharp.dll'), '/out:'+str(out/'WildChickenIsChicken.dll'),source])
    run([a.mcs,'/noconfig','/reference:'+str(out/'Assembly-CSharp.dll'),'/reference:'+str(out/'WildChickenIsChicken.dll'),'/out:'+str(out/'Runner.exe'),root/'Runner.cs'])
    print(variant + '\n' + run([a.mono,out/'Runner.exe'], root/(variant+'.log')))
out=root/'stale-binary';out.mkdir(exist_ok=True)
shutil.copy2(root/'new-property/Assembly-CSharp.dll',out/'Assembly-CSharp.dll')
for filename in ('WildChickenIsChicken.dll','Runner.exe'): shutil.copy2(root/'old-field'/filename,out/filename)
print('stale-binary\n' + run([a.mono,out/'Runner.exe','expect-mismatch'],root/'stale-binary.log'))
(root/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
(root/'summary.json').write_text(json.dumps({'game_executed':False,'actual_action_source':str(source),'old_field_api_checks':11,'new_property_api_checks':11,'stale_binary_holdingEntity_failure_reproduced':True,'presentation_tested':False,'fixture_is_not_the_game':True},indent=2)+'\n')
