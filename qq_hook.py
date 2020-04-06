import requests
from const.Hook_api import *

class Hook():
    def __init__(self,num):
        if num==1:
            self.api=api_1
        elif num==2:
            self.api=api_2
        else:
            self.api=str(num)

    def send(self,text):
        data=('{"content":[{"type":0,"data":"'+text+'"}]}').encode()
        try:
            resp=requests.post(self.api,data)
            print(resp.text)
        except Exception as e:
            print(f'\033[37;41mHook:error[{str(e)}]\033[0m')

