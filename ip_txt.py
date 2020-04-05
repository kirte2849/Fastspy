import requests
import telnetlib
from threading import Lock,Thread
from apis import Apis
from random import choice

t_num=30
results=[]
l=Lock()
apis=Apis()
spis.timeout=5

def cut(text,num):#将列表text分为num份
    if len(text)<num:
        print('\033[1;33m['+str(num)+' is too big.]\033[0m')
    if len(text)%num!=0:
        t=len(text)//num+1
    else:
        t=len(text)/num
    t=int(t)
    s=[]
    for i in range(0,len(text),t):
        b=text[i:i+t]
        s.append(b)
    return s

def multi_thread(func,args,num):
        t=[]
        args=cut(args,num)
        for each in range(len(args)):
            temp=Thread(target=func,args=(each,args[each]))
            temp.start()
            t.append(temp)
        for each in t:
            each.join()

def telnet_check(ip,port):
    try:
        #print(ip,port)
        telnetlib.Telnet(ip, port=port, timeout=3)
    except Exception as e:
        #print(str(e))
        #print('\033[1;31mtelnet_check:failed\033[0m') 
        return 0
    else:   
        #print('\033[1;31mtelnet_check:success\033[0m')            
        return 1

def main(id,prs):
    global results
    r=[]
    print(str(id)+' runing')
    for each in prs:
        if telnet_check(each.split(':')[0],each.split(':')[1]):
            if getattr(apis,choice(apis.api_names))(each):
                print(f'\033[1;36mCongratulations!   {each} Succesful!\033[0m')
                r.append(each)
    l.acquire()
    results+=r
    l.release()
    
prs=[]
f=open('src/prs.txt','r')
for each in f:
    prs.append(each.strip('\n',).strip())
f.close()
multi_thread(main,prs,t_num)
f=open('result/result.txt','w')
for each in results:
    f.write(each)
f.close()










