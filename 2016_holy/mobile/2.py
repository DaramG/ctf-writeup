import pwnbox,string,sys
def do(data):
  p =pwnbox.pipe.SocketPipe("1.224.175.16",10101)
  for i in range(len(data)):
    q = str(i+1)+data[:i+1]
    p.write(q)
    ret = p.read_byte(1) != "?"
    if ret:
      p.read_byte(len(q)-1)
  p.close()
  return ret

data = "2o16}"
print do(data)
"""
for i in range(5):
  done = False
  for x in string.printable:
    if do(data+x):
      data += x
      print data
      done = True
      break
  if not done:
    print "ERROR"
    sys.exit(-1)

"""
