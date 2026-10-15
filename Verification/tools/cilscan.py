"""Read-only CIL operand scanning for emitted-call validation (no execution)."""
import struct
ONE={**{x:1 for x in range(0x0e,0x14)},0x1f:1,0x20:4,0x21:8,0x22:4,0x23:8,0x27:4,0x28:4,0x29:4,**{x:1 for x in range(0x2b,0x38)},**{x:4 for x in range(0x38,0x45)},**{x:4 for x in range(0x6f,0x76)},0x79:4,**{x:4 for x in range(0x7b,0x82)},0x8c:4,0x8d:4,0x8f:4,0xa3:4,0xa4:4,0xa5:4,0xc2:4,0xc6:4,0xd0:4,0xdd:4,0xde:1}
TWO={0x06:4,0x07:4,**{x:2 for x in range(0x09,0x0f)},0x12:1,0x15:4,0x16:4,0x19:1,0x1c:4}
VALID_ONE=set(range(0x00,0x24))|set(range(0x25,0x77))|set(range(0x79,0xa6))|set(range(0xb3,0xbb))|{0xc2,0xc3,0xc6}|set(range(0xd0,0xe1))
VALID_TWO=set(range(0x00,0x08))|set(range(0x09,0x10))|set(range(0x11,0x1b))|{0x1c,0x1d,0x1e}
def body(c,mid):
 rva=c.rows[6][mid][0]
 if not rva:return b''
 p=c.off(rva);d=c.data
 if d[p]&3==2:size=d[p]>>2;p+=1
 elif d[p]&3==3:
  h,_,size,_=struct.unpack_from('<HHII',d,p);p+=(h>>12)*4
 else:raise ValueError('Invalid CIL header '+hex(rva))
 return d[p:p+size]
def instructions(d):
 p=0
 while p<len(d):
  offset=p;op=d[p];p+=1
  if op==0xfe:
   sub=d[p];p+=1
   if sub not in VALID_TWO:raise ValueError('Unknown two-byte opcode '+hex(sub))
   width=TWO.get(sub,0);op=0xfe00|sub
  elif op==0x45:
   count=struct.unpack_from('<I',d,p)[0];width=4+4*count
  else:
   if op not in VALID_ONE:raise ValueError('Unknown opcode '+hex(op))
   width=ONE.get(op,0)
  operand=d[p:p+width]
  if len(operand)!=width:raise ValueError('Truncated CIL operand')
  p+=width;yield offset,op,operand
