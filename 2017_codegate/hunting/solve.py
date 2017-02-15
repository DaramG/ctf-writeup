import subprocess,os,sys,time
RAND = []
def write(data):
  p.stdin.write(data)
  p.stdin.flush()
def read_byte(n):
  ret = ""
  for i in range(n):
    ret+=p.stdout.read(1)
  return ret

def read_until(data):
  ret = ""
  while True:
    ret += p.stdout.read(1)
    if data in ret: break
  print ret
  return ret
def interact():
  return p.communicate()

def get_rand():
  ret = []
  with open("rand","rb") as f:
    tmp=f.read().split("\n")[:-1][::-1]
    for x in tmp:
      ret.append(int(x))
  return ret

def rand():
  global RAND
  return RAND.pop()

def get_defense():
  r=rand() % 4
  if r==1: return 3
  elif r==2: return 2
  elif r==0: return 1
  return 3

p = subprocess.Popen("stdbuf -i0 -o0 -e0 ./hunting".split(" "),stdin=subprocess.PIPE,stdout=subprocess.PIPE)
os.system("./get >rand")
RAND = get_rand()
def change(n):
  ret = ""
  if n!=7:
    ret = read_until("Exit")
  write("3\n")
  write("%d\n"%n)
  return ret

def attack(flag = True):
  ret = ""
  if flag:
    ret = read_until("Exit")
  write("2\n")
  if flag:
    time.sleep(0.2)
    rand()
  write("%d\n"%get_defense())
  if flag:
    return ret+read_until("6.")
  else: return ret

change(3)
lv = 0
for i in range(50):
  tmp = attack()
  if "level" in tmp:
    lv +=1
  if lv == 3:
    break
change(2)
attack(True)
time.sleep(0.2)
change(7)
attack(True)
time.sleep(2)

change(2)
attack(True)
time.sleep(0.2)
change(7)
attack(True)
time.sleep(1)
print "DONE"
print interact()[0]

