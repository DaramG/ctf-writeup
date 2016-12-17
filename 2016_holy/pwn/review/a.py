with open("v","rb") as f:
  data =f.read()
  cnt = 0
  a = ""
  for x in data.split("\n")[:-1]:
    a+=x+"\n"
    if "add" in x and cnt ==0:
      add = x
    if "ret" in x:
      if "$0x" in add and add != "":
        v = int(add.split("$0x")[1].split(",")[0],16)/4
      else:
        v = 0
      cnt +=v
      if cnt ==7:
        print a
        print cnt
      cnt = 0
      add = ""
      a = ""
    elif "pop" in x:
      cnt +=1
