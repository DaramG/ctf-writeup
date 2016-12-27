import md5
a=[[23,33,92,67],[75,64,95,78],[61,89,10,16],[12,77,45,58]]
ret = ""
for b in a:
  for x in b:
    ret += str(x)
print ret
print  md5.new(ret).digest().encode("hex")
