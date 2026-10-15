"""Read-only PE/ECMA-335 metadata inspection. Does not load or execute assemblies."""
import struct,sys,hashlib,json,uuid
class CLR:
 def __init__(self,path):
  self.path=path; self.data=open(path,'rb').read(); d=self.data
  pe=struct.unpack_from('<I',d,0x3c)[0]; assert d[pe:pe+4]==b'PE\0\0'
  nsec=struct.unpack_from('<H',d,pe+6)[0]; optsize=struct.unpack_from('<H',d,pe+20)[0]; opt=pe+24; magic=struct.unpack_from('<H',d,opt)[0]; dd=opt+(96 if magic==0x10b else 112)
  self.sections=[struct.unpack_from('<8sIIIIIIHHI',d,opt+optsize+i*40) for i in range(nsec)]
  cli=self.off(struct.unpack_from('<I',d,dd+14*8)[0]); meta=self.off(struct.unpack_from('<I',d,cli+8)[0]); assert d[meta:meta+4]==b'BSJB'
  vl=struct.unpack_from('<I',d,meta+12)[0]; self.runtime=d[meta+16:meta+16+vl].split(b'\0')[0].decode(); pos=meta+16+vl; pos=(pos+3)&~3
  flags,nstream=struct.unpack_from('<HH',d,pos); pos+=4; streams={}
  for i in range(nstream):
   so,sz=struct.unpack_from('<II',d,pos); end=d.index(0,pos+8); name=d[pos+8:end].decode(); pos=(end+4)&~3; streams[name]=d[meta+so:meta+so+sz]
  self.streams=streams; self.strings=streams['#Strings']; self.blobs=streams['#Blob']; self.guids=streams.get('#GUID',b''); tab=streams.get('#~',streams.get('#-')); self.tab=tab
  _,major,minor,hs,_=struct.unpack_from('<IBBBB',tab,0); valid,sorted_=struct.unpack_from('<QQ',tab,8); pos=24; self.count={}
  for i in range(64):
   if valid>>i&1:self.count[i]=struct.unpack_from('<I',tab,pos)[0];pos+=4
  self.heap_width={'s':4 if hs&1 else 2,'g':4 if hs&2 else 2,'b':4 if hs&4 else 2}
  self.coded={
   'TypeDefOrRef':(2,[2,1,27]),'HasConstant':(2,[4,8,23]),'HasCustomAttribute':(5,[6,4,1,2,8,9,10,0,14,23,20,17,26,27,32,35,38,39,40,42,44,43]),
   'HasFieldMarshal':(1,[4,8]),'HasDeclSecurity':(2,[2,6,32]),'MemberRefParent':(3,[2,1,26,6,27]),'HasSemantics':(1,[20,23]),'MethodDefOrRef':(1,[6,10]),
   'MemberForwarded':(1,[4,6]),'Implementation':(2,[38,35,39]),'CustomAttributeType':(3,[None,None,6,10,None]),'ResolutionScope':(2,[0,26,35,1]),'TypeOrMethodDef':(1,[2,6])}
  self.schema={0:'u2 s g g g',1:'ResolutionScope s s',2:'u4 s s TypeDefOrRef t4 t6',3:'t4',4:'u2 s b',5:'t6',6:'u4 u2 u2 s b t8',7:'t8',8:'u2 u2 s',9:'t2 TypeDefOrRef',10:'MemberRefParent s b',11:'u2 HasConstant b',12:'HasCustomAttribute CustomAttributeType b',13:'HasFieldMarshal b',14:'u2 HasDeclSecurity b',15:'u2 u4 t2',16:'u4 t4',17:'b',18:'t2 t20',19:'t20',20:'u2 s TypeDefOrRef',21:'t2 t23',22:'t23',23:'u2 s b',24:'u2 t6 HasSemantics',25:'t2 MethodDefOrRef MethodDefOrRef',26:'s',27:'b',28:'u2 MemberForwarded s t26',29:'u4 t4',30:'u4 u4',31:'u4',32:'u4 u2 u2 u2 u2 u4 b s s',33:'u4',34:'u4 u4 u4',35:'u2 u2 u2 u2 u4 b s s b',36:'u4 t35',37:'u4 u4 u4 t35',38:'u4 s b',39:'u4 u4 s s Implementation',40:'u4 u4 s Implementation',41:'t2 t2',42:'u2 u2 TypeOrMethodDef s',43:'MethodDefOrRef b',44:'t42 TypeDefOrRef'}
  self.rows={}; self.table_offsets={}
  for i in range(64):
   if i not in self.count:continue
   self.table_offsets[i]=pos; specs=self.schema[i].split(); widths=[self.width(x) for x in specs]; size=sum(widths); fmt='<'+''.join('I' if w==4 else 'H' for w in widths)
   self.rows[i]=[None]+[struct.unpack_from(fmt,tab,pos+j*size) for j in range(self.count[i])];pos+=self.count[i]*size
  self.nested={row[0]:row[1] for row in self.rows.get(41,[])[1:]}; self.method_owner={};self.field_owner={}
  for i,row in enumerate(self.rows.get(2,[])[1:],1):
   nextrow=self.rows[2][i+1] if i<self.count[2] else None
   for j in range(row[5],nextrow[5] if nextrow else self.count.get(6,0)+1):self.method_owner[j]=i
   for j in range(row[4],nextrow[4] if nextrow else self.count.get(4,0)+1):self.field_owner[j]=i
 def off(self,rva):
  for s in self.sections:
   _,vs,va,rs,rp,*_=s
   if va<=rva<va+max(vs,rs):return rva-va+rp
  raise ValueError(rva)
 def width(self,s):
  if s=='u2':return 2
  if s=='u4':return 4
  if s in self.heap_width:return self.heap_width[s]
  if s.startswith('t'):return 4 if self.count.get(int(s[1:]),0)>65535 else 2
  bits,ts=self.coded[s];return 4 if any(self.count.get(t,0)>=(1<<(16-bits)) for t in ts if t is not None) else 2
 def string(self,i):return self.strings[i:self.strings.index(0,i)].decode('utf-8',errors='replace')
 @staticmethod
 def uint(d,p):
  a=d[p]
  if a<128:return a,p+1
  if a<192:return ((a&63)<<8)|d[p+1],p+2
  if a<224:return ((a&31)<<24)|(d[p+1]<<16)|(d[p+2]<<8)|d[p+3],p+4
  raise ValueError('Bad compressed integer')
 def blob(self,i):
  n,p=self.uint(self.blobs,i);return self.blobs[p:p+n]
 def decode(self,s,v):
  bits,ts=self.coded[s];return ts[v&((1<<bits)-1)],v>>bits
 def typename(self,t,i):
  if not i:return '<null>'
  row=self.rows[t][i]
  if t==27:return self.type_sig(self.blob(row[0]),0)[0]
  if t==2:
   n=self.string(row[1]); ns=self.string(row[2]);return (self.typename(2,self.nested[i])+'+'+n) if i in self.nested else (ns+'.' if ns else '')+n
  if t==1:
   n=self.string(row[1]);ns=self.string(row[2]);return (ns+'.' if ns else '')+n
  return f'table{t}:{i}'
 def type_sig(self,d,p):
  et=d[p];p+=1
  primitives={1:'void',2:'bool',3:'char',4:'int8',5:'uint8',6:'int16',7:'uint16',8:'int32',9:'uint32',10:'int64',11:'uint64',12:'float32',13:'float64',14:'string',22:'typedref',24:'native int',25:'native uint',28:'object'}
  if et in primitives:return primitives[et],p
  if et in (15,16,29,69):
   n,p=self.type_sig(d,p);return n+{15:'*',16:'&',29:'[]',69:' pinned'}[et],p
  if et in (17,18):
   tok,p=self.uint(d,p);return self.typename(*self.decode('TypeDefOrRef',tok)),p
  if et in (19,30):
   n,p=self.uint(d,p);return ('!' if et==19 else '!!')+str(n),p
  if et==21:
   n,p=self.type_sig(d,p);count,p=self.uint(d,p);args=[]
   for _ in range(count):a,p=self.type_sig(d,p);args.append(a)
   return n+'<'+', '.join(args)+'>',p
  if et in (31,32):
   tok,p=self.uint(d,p);mod=self.typename(*self.decode('TypeDefOrRef',tok));n,p=self.type_sig(d,p);return n+(' modreq(' if et==31 else ' modopt(')+mod+')',p
  if et==20:
   n,p=self.type_sig(d,p);rank,p=self.uint(d,p);sz,p=self.uint(d,p)
   for _ in range(sz):_,p=self.uint(d,p)
   lb,p=self.uint(d,p)
   for _ in range(lb):_,p=self.uint(d,p)
   return n+'['+','*(rank-1)+']',p
  if et==27:return 'fnptr('+d[p:].hex()+')',len(d)
  if et==65:return '...',p
  raise ValueError('Unhandled element '+str(et)+' at '+str(p-1)+' '+d.hex())
 def signature(self,idx):
  d=self.blob(idx);p=1;cc=d[0]
  try:
   if cc==6:return self.type_sig(d,p)[0]
   generic=0
   if cc&16:generic,p=self.uint(d,p)
   count,p=self.uint(d,p);ret,p=self.type_sig(d,p);args=[]
   for _ in range(count):a,p=self.type_sig(d,p);args.append(a)
   return ('instance ' if cc&32 else 'static ')+ret+' ('+', '.join(args)+')'+(f' generic({generic})' if generic else '')
  except Exception as e:return 'RAW '+d.hex()+' ERROR '+str(e)
 def types(self,query=None):return [(i,self.typename(2,i)) for i in range(1,self.count.get(2,0)+1) if query is None or query.lower() in self.typename(2,i).lower()]
 def type_report(self,i):
  row=self.rows[2][i];name=self.typename(2,i);nxt=self.rows[2][i+1] if i<self.count[2] else None
  out={'token':hex(0x02000000|i),'name':name,'flags':hex(row[0]),'base':self.typename(*self.decode('TypeDefOrRef',row[3])),'fields':[],'methods':[],'properties':[]}
  for j in range(row[4],nxt[4] if nxt else self.count.get(4,0)+1):
   f=self.rows[4][j];out['fields'].append({'token':hex(0x04000000|j),'name':self.string(f[1]),'flags':hex(f[0]),'signature':self.signature(f[2])})
  for j in range(row[5],nxt[5] if nxt else self.count.get(6,0)+1):
   f=self.rows[6][j];out['methods'].append({'token':hex(0x06000000|j),'rva':hex(f[0]),'name':self.string(f[3]),'flags':hex(f[2]),'signature':self.signature(f[4])})
  maps=self.rows.get(21,[])
  for j,m in enumerate(maps[1:],1):
   if m[0]!=i:continue
   end=maps[j+1][1] if j<self.count[21] else self.count.get(23,0)+1
   for k in range(m[1],end):
    f=self.rows[23][k];out['properties'].append({'token':hex(0x17000000|k),'name':self.string(f[1]),'flags':hex(f[0]),'signature':self.signature(f[2])})
  return out
 def identity(self):
  a=self.rows.get(32,[None,None])[1];m=self.rows.get(0,[None,None])[1]
  return {'path':self.path,'sha256':hashlib.sha256(self.data).hexdigest(),'runtime':self.runtime,'assembly':self.string(a[7]) if a else None,'version':'.'.join(map(str,a[1:5])) if a else None,'mvid':str(uuid.UUID(bytes_le=self.guids[(m[2]-1)*16:m[2]*16])) if m else None}
if __name__=='__main__':
 c=CLR(sys.argv[1]);print(json.dumps(c.identity(),indent=2));qs=sys.argv[2:]
 for q in qs:
  for i,n in c.types(q):
   if n==q or len(c.types(q))<5: print(json.dumps(c.type_report(i),indent=2))
