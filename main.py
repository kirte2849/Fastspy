from fastspy import spyder,insert
import fastspy as spy

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
		img=html.xpath('//img [@alt]')
		for each in img:
			r.append(each.attrib['src'])
		title=html.xpath('//title')[0].text
		return {'title':title,'img_src':r}
	except Exception as e:
		insert(repr(e))
		return {'title':'null','img_src':'null'}
		
def func_1_next(html,url):
	#在这里返回url_1的下一页url
	a=url.split('/')[-1].split('.')[0]
	r='https://qqc962.com/page/'+str(int(a)+1)+'.html'
	return r
	
def func_1_search(html,url):
	r=[]
	a=html.xpath('//a [@class="thumbnail"]')[:10]
	for each in a:
		r.append(spy.main_url+each.attrib['href'][1:])
	#在这里返回url_2的列表
	return r
	
def func_2_next(html,url):
	#在这里返回url_2的下一页
	try:
		a=html.xpath('//div [@class="pagination pagination-multi"]')[0][0][-1][0].attrib['href']
		return url[:url.rfind('/')]+'/'+a
	except Exception as e:
		insert(str(e))
		return 0
	
#@@@@@@@@@@@@@@@@@@@@@@@@#
#@@@@@@@@@@@@@@@@@@@@@@@@#

#######常量#######
spy.out_file='out.txt'#输出文件
spy.log_file='url1.log'#日志文件
spy.thread_num=3#线程数
spy.main_url='https://qqc962.com/'#首页
url='https://qqc962.com/page/1.html'#从第几页开始爬
#################

if __name__ == '__main__':
	spy.func_2_search,spy.func_2_next,spy.func_1_search,spy.func_1_next=func_2_search,func_2_next,func_1_search,func_1_next
	spy.main(url,1)#main(从第几页开始，爬几页)



















