class Main_settings():
    '''储存main的所有设置'''

    def __init__(self):

        self.out = 'results/result.main'#输出文件名

        self.log = 'results/url_1.log.main'#日志文件名

        self.thread_num = 10#线程数

        self.main_url = 'https://qqc962.com/'#首页

        self.url = 'https://qqc962.com/page/1.html'#从第几页开始爬

        self.header = None

        self.pr_use = 'on'

        self.db_port = 6379

        self.db_ip='127.0.0.1'

        self.db_pw=''

        self.db_db='0'
    
##hook
class Qq_hook_settings():
    def __init__(self):
    
        self.api_1='https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=c566电脑版得很6fe3aeae9080ef55e123fcb'#修改
        
        self.api_2='https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=363139ea2161aff4都不时间你是不是快de6d'#请修改
##