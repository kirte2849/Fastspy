from fastspy import spyder,insert,noerror
import fastspy as spy
from lxml import etree
import re
from settings import Main_settings
'''
_author=kirte
_date=2020.3.16

代码结构：
def func_2_search
def func_1_next
def func_1_search
def func_2_next
'''


#@@@@@@@你只需要修改这里@@@@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@#
def func_2_search(html,url):
    #在这里返回url_2的资源字典
    r=[]
    try:
        payload=r'''<p><img src="https:.+?"'''
        result=re.findall(payload,html)
        title=re.search(r"<title>.*</title>",html).group(0)[7:-8]
        r=[]
        for each in result:
            r.append(each.replace(r'"',"")[12:])
        return {'title':title,'img_src':r}#这些返回的数据会被fastspy加到一个叫src的变量中，src的结构[{'title':title,'img_src':r},{'title':title,'img_src':r}......省略]
    except Exception as e:
        insert('\033[37;41mError at [func_2_srarch]:'+str(e)+'\033[0m')
        return {'title':'null','img_src':'null'}
        
@noerror
def func_1_next(html,url):#这里的html为none
    #在这里返回url_1的下一页url
    a=url.split('/')[-1].split('.')[0]
    r='https://qqc962.com/page/'+str(int(a)+1)+'.html'
    return r
    
@noerror
def func_1_search(html,url):
    r=re.findall(r'''<h2><a target="_blank" href=".*?\.html''',html)
    a=[]
    for each in r:
        r2=each[each.find("href")+7:]
        a.append(spy.main_url+r2)
    return a

@noerror
def func_2_next(html,url):
    #在这里返回url_2的下一页
    i=re.findall(r"next-page.*?下一页",html)
    if i==[]:
        return 0
    i=i[0]
    if url.find("_")!=-1:
        #print("有_")
        r=i[i.find("href")+6:-5]
        next=url[:url.find("_")-4]+r
        return next        
    r=i[i.find("_")-4:-5]
    next=url[:url.find("html")-5]+r
    return next

def func_save(src,out_file):
    with open(out_file,'w',encoding='utf-8') as f:
        for each in src:
            try:
                f.write(str(each)+'\n')
            except Exception as e:
                insert('\033[37;41m'+str(e)+'\033[0m')
        insert('保存完毕')
#@@@@@@@@@@@@@@@@@@@@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@#

#######常量#######
settings = Main_settings()
spy.out_file = settings.out
spy.log_file = settings.log
spy.thread_num = settings.thread_num
spy.main_url = settings.main_url
url = settings.url
spy.header = settings.header
spy.pr_use = settings.pr_use
spy.db_port = settings.db_port
spy.db_ip = settings.db_ip
spy.db_pw = settings.db_pw
spy.db_db = settings.db_db
#################

if __name__ == '__main__':
    spy.func_2_search,spy.func_2_next,spy.func_1_search,spy.func_1_next=func_2_search,func_2_next,func_1_search,func_1_next
    spy.func_save=func_save
    spy.main(url,1)#main(从第几页开始，爬几页)



















