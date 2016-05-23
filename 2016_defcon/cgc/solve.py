import pwnbox
with open("./legit_0003_patch","rb") as f: data = f.read()
p= pwnbox.pipe.SocketPipe("legit_00004_patch_c87784d25829f281e6d0205eaac5da7c.quals.shallweplayaga.me",23274)
p.read_until("?")
p.write("%d\n"%len(data))
p.read_until("\n")
p.write(data)
p.interact()

