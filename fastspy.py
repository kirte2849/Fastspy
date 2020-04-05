from threading import Thread,Lock
import redis
import random
from time import sleep
import sys
import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
_author=kirte
_date=2020.3.16
'''

proc_now=0
proc_all=20
process_num=20
sep=1.7#刷新速度
stop=1
main_url='http://bbs.tjdige.com/'
url_1=[]
url_2=[]
thread_num=2
func_1_next=1
func_1_search=1
func_2_next=1
func_2_search=1
func_save=1
out_file='out.txt'
log_file='url.log'
l=Lock()
src=[]
header=None
timeout=5
pr_use='off'
db_port=6379
db_ip='127.0.0.1'
db_pw=''
db_db='0'





def noerror(func):
    def zsq(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print(f'\033[37;41m{"-"*40}\n\n\n\n\n\n一个错误出现在函数'+func.__name__+'\n错误类型:['+str(e)+']')
            print(f'我们正在尽全力进行挽回...\n\n\n\n\n{"-"*40}\n\033[0m')
            return None
    return zsq

def draw(process,num):#绘制进度条，当前进度process，总进度num
    print(">>进度:",end="")
    print("■"*process+"□"*(num-process)+str(process)+"/"+str(num)+"                      \r",end='')
    
def insert(string):
    num=int((proc_now/proc_all)*process_num)
    print(string+"                           ")
    draw(num,process_num)

def job():
    global proc_now,proc_all
    while stop:
        num=int((proc_now/proc_all)*process_num)
        draw(num,process_num)
        sleep(sep)
    
def start():
    t=Thread(target=job)
    t.setDaemon(True)
    t.start()

def pipe(host='127.0.0.1',db='0',pw=''):
    r=redis.Redis(host=host,port='6379',db=db,password=pw,decode_responses=True)
    pro=random.choice(r.keys())
    proxy={'http' : pro
           ,'https':pro}
    return proxy


def spyder(url,pro='off',down='off',meta=False):
    times=0
    while True:
        try:
            if pro == 'off' :
                if header:
                    insert('使用header')
                    resp=requests.get(url=url,timeout=timeout, verify=False,headers=header)
                else:
                    resp=requests.get(url=url,timeout=timeout, verify=False)
            elif pro == 'on' :
                proxy=pipe()
                if header:
                    resp=requests.get(url=url,proxies=proxy,timeout=5,headers=header,verify=False)
                else:
                    resp=requests.get(url=url,proxies=proxy,timeout=5, verify=False)
                print('使用代理成功' + str(proxy))
            if resp.status_code != 200 :
                insert(f'\033[1;31m[{url}:\033[1;33m错误代码:{resp.status_code}\033[1;31m]\033[0m' )
                if times>=3:
                    insert(f'\033[37;41m{"-"*40}\n错误次数过多，放弃重试......\n{"-"*40}\n\033[0m')
                    break
                else:
                    times+=1
                    continue
            if len(resp.text) < 2 :
                print('[返还数据为空!]')
                continue
        except Exception as e:
            insert(f'\033[1;33m{type(e)}:\033[1;31m{str(e)}\033[0m')
            times+=1
            sleep(0.5)
            if times>=3:
                insert(f'\033[37;41m{"-"*40}\n错误次数过多，放弃重试......\n{"-"*40}\033[0m')
                break
            else:
                sleep(0.5)
        else:
            source_encoding = resp.apparent_encoding or resp.encoding
            if down == 'off' :
                insert('\033[1;36m[gethtml:'+str(url)+']\033[0m')
                return resp.content.decode(source_encoding, errors="ignore")
            elif down == 'on' :
                return resp.content
         
def down(url,name='null',mod='txt'):
    datas=spyder(url,'off','on')
    if name == 'null' :
        name=os.path.basename(url)
    if mod == 'txt' :
        write_txt(name,datas)
    elif mod == 'picv' :
        write_picv(name,datas)

def write_txt(name,datas):
    with open(name,'wb') as f:
        f.write((datas).decode().encode())
        f.close()
        
def write_picv(name,datas):
    with open(name,'wb') as f:
        f.write(datas)
        f.close()
        
def mkdir(name):
    if not os.path.isdir(name):
        os.mkdir(name)

def cd(name):
    if os.path.isdir(name):
        os.chdir(name)
        
def cut(text,num):#将列表text分为num份
    if len(text)<num:
        insert('\033[1;33m['+str(num)+' is too big.]\033[0m')
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
    
def t_func(id,url_list):
    global src,process,proc_now
    src_temp=[]
    insert('[线程'+str(id)+'运行]')
    for each in url_list:
        next_page=each
        while next_page:
            html=spyder(next_page,pr_use)
            src_temp.append(func_2_search(html,next_page))
            next_page=func_2_next(html,next_page)
        insert('url_2完成爬行:'+str(each))
        l.acquire()
        proc_now=proc_now+1
        l.release()
    l.acquire()        
    src=src+src_temp
    l.release()
    
def multi_thread(func,args,num):
        t=[]
        args=cut(args,num)
        for each in range(len(args)):
            temp=Thread(target=func,args=(each,args[each]))
            temp.start()
            t.append(temp)
        for each in t:
            each.join()
            
def main (url_start='http://bbs.tjdige.com/list.asp?p=1&classid=6',num=0):
    global url_1,url_2,src,proc_all
    i=0
    url_now=url_start
    html=''
    print('\033[1;32m主页:'+str(main_url))
    print('开始url:'+url_start)
    print('线程数:'+str(thread_num))
    print('url_2输出文件:'+log_file)
    print('输出结果文件:'+out_file)
    insert('\033[1;31m------------------第一阶段-----------------\033[0m')
    start()
    f=open(log_file,'a',encoding='utf-8')
    for i in range(num+1):
        insert('正在寻找url_1:'+str(url_now))
        html=spyder(url_now,pr_use)
        a=func_1_search(html,url_now)
        for each in a:
            f.write(each+'\n')
        url_2=url_2+a
        url_1.append(url_now)
        url_now=func_1_next(None,url_now)
        if url_now==False:
            insert('\033[1;32murl_1没有下一页了')
            break
    f.close()
    insert('\033[1;32m爬至'+str(url_now))
    insert('共'+str(len(url_2))+'部')
    proc_all=len(url_2)
    insert('\033[1;31m------------------第2阶段-----------------\033[1;32m')
    multi_thread(t_func,args=url_2,num=thread_num)
    insert('正在保存…\033[1;32m')
    func_save(src,out_file)
    quit()
        

if __name__ == '__main__':
    print('这是一个模块，你不能这样打开')
    input('输入回车来结束') 


            

        
    
        

























