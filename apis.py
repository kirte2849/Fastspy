import requests


class Apis():
    def __init__(self):
        self.timeout=5
        self.api_names=['api_check_1'
                    ,'api_check_2'
                    
                    
                    
                    
                    ]

    def api_check_1(self,pr):
        #print('you used me'+'api_check_1')
        proxies = {
          'http': 'http://'+pr,
          'https': 'http://'+pr,
        }
        try:
            resp=requests.get('https://api.ipify.org/',timeout=self.timeout, proxies=proxies)
            if resp.content.decode()==pr.split(':')[0]:
                return True
            else:
                return False
        except Exception as e:
            print(f'\033[1;31mapi_check:{pr} timeout\033[0m')
            return False
    
    def api_check_2(self,pr):
        #print('you used me'+'api_check_2')
        proxies = {
          'http': 'http://'+pr,
          'https': 'http://'+pr,
        }
        try:
            resp=requests.get('http://icanhazip.com/',timeout=self.timeout, proxies=proxies)
            if resp.content.decode()==pr.split(':')[0]:
                return True
            else:
                return False
        except:
            print(f'\033[1;31mapi_check:{pr} timeout\033[0m')
            return False
    