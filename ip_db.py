import requests
import telnetlib
from threading import Lock,Thread
from apis import Apis
from random import choice
import redis

t_num=50
apis=Apis()
tel_timeout=5
apis.timeout=7
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,max_connections=200)
num=0
l=Lock()


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
        telnetlib.Telnet(ip, port=port, timeout=1.5)
        return True
    except Exception as e:
        #print(str(e))
        #print(f'\033[1;31m{ip}telnet_check:failed\033[0m') 
        return 0

def main(id,prs):
    global results,num
    conn = redis.Redis(connection_pool=pool,decode_responses=True)
    r=[]
    print(str(id)+' runing')
    for each in prs:
        if telnet_check(each.split(':')[0],each.split(':')[1]):
            if getattr(apis,choice(apis.api_names))(each):
                print(f'\033[1;36mCongratulations!   {each} Succesful!\033[0m')
                conn.set(each,0)
                print(f'[redis:{each} 写入]')
                l.acquire()
                num+=1
                l.release()
prs=[]
f=open('prs.txt','r')
for each in f:
    prs.append(each.strip('\n',).strip())
f.close()
prelen=len(prs)
prs=list(set(prs))
aftlen=len(prs)
multi_thread(main,prs,t_num)
print('\033[1;36m完毕')
print(f'\033[1;36m输入数据{str(prelen)}条')
print(f'重复数据{str(prelen-aftlen)}条')
print(f'有效输入数据{str(aftlen)}条')
print(f'本次录入{str(num)}条')








