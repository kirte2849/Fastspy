from threading import Thread,Lock
import redis
import random
from time import sleep
import sys

proc_now=0
proc_all=20
process_num=20
sep=0.1#刷新速度
stop=1
main_url='http://bbs.tjdige.com/'
url_1=[]
url_2=[]
thread_num=1
func_1_next=1
func_1_search=1
func_2_next=1
func_2_search=1
out_file='out.txt'
log_file='url.log'
l=Lock()
src=[]


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
    proxy={'http' : pro}
    return proxy

import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def spyder(url,pro='off',down='off'):
    while True:
        try:
            if pro == 'off' :
                resp=requests.get(url=url,timeout=10, verify=False)
            elif pro == 'on' :
                proxy=pipe()
                resp=requests.get(url=url,proxies=proxy,timeout=10, verify=False)
                print('使用代理成功' + str(proxy))
            if resp.status_code != 200 :
                print('[错误的返还码:' + resp.status_code + '!]')
                continue
            if len(resp.text) < 2 :
                print('[返还数据为空!]')
                continue
        except:
            insert('[请求超时!]' )
            sleep(0.5)
        else:
            source_encoding = resp.apparent_encoding or resp.encoding
            if down == 'off' :
                return etree.HTML(resp.content.decode(source_encoding, errors="ignore"))
                break
            elif down == 'on' :
                return resp.content
                break
                
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
		insert('['+str(num)+' is too big.]')
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
	for each in url_list:
		insert(each)
		l.acquire()
		proc_now=proc_now+1
		l.release()
		next_page=each
		while next_page:
			html=spyder(next_page)
			src_temp.append(func_2_search(html))
			next_page=func_2_next(html)
	l.acquire()
	src=src+src_temp
	l.release()
	
def multi_thread(func,args,num):
		t=[]
		args=cut(args,num)
		for each in range(num):
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
	print('主页:'+main_url)
	print('开始url:'+url_start)
	print('线程数:'+str(thread_num))
	print('url_2输出文件:'+log_file)
	print('输出结果文件:'+out_file)
	print('第一阶段')
	start()
	f=open(log_file,'a',encoding='utf-8')
	for i in range(num+1):
		insert(url_now)
		html=spyder(url_now)
		a=func_1_search(html)
		for each in a:
			f.write(each+'\n')
		url_2=url_2+a
		url_1.append(url_now)
		url_now=func_1_next(url_now)
	f.close()
	insert('爬至'+url_now)
	insert('共'+str(len(url_2))+'部')
	proc_all=len(url_2)
	insert('第二阶段')
	multi_thread(t_func,args=url_2,num=thread_num)
	insert('正在保存…')
	with open(out_file,'w',encoding='utf-8') as f:
		for each in src:
			try:
				f.write(str(each)+'\n')
			except Exception as e:
				insert(str(e))
		insert('保存完毕')
		quit()
		
		

			

		
	
		

























