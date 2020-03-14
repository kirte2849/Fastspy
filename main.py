
from fastspy import spyder
import fastspy as spy


def func_2_search(html):
	try:
		temp=html.xpath('//span [@style="font-size:14px;"]/..')
		title=html.xpath('//title')[0].text.split('|')[0]
		img_src=html.xpath('//meta [@property="og:image"]')[0].attrib['content']
		bd=temp[0][1][0].text+'_&&_'+temp[0][2][0].text
		ot=temp[1][1][0].text
		return {'title':title,'img_src':img_src,'bd':bd,'ot':ot}
	except Exception as e:
		print(repr(e))
		return {'title':'null','img_src':'null','bd':'null','ot':'null'}
def func_1_next(url):
	now=url[url.find('?')+3:url.find('&')]
	r='http://bbs.tjdige.com/list.asp?p='+str(int(now)+1)+'&classid=8'
	return r
	
def func_1_search(html):
	t=[]
	r=html.xpath(r"//a [@target='_parent' and @class='title']")
	for each in r:
		t.append(spy.main_url+each.attrib['href'])
	return t
	
def func_2_next(html):
	return 0

#######常量#######
spy.out_file='out.txt'
spy.log_file='url.log'
spy.thread_nun=15
spy.main_url='http://bbs.tjdige.com/'
#################
url='http://bbs.tjdige.com/list.asp?p=1&classid=9'
spy.func_2_search,spy.func_2_next,spy.func_1_search,spy.func_1_next=func_2_search,func_2_next,func_1_search,func_1_next
spy.main(url,3)



















