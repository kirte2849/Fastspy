import requests

class Hook():
    def __init__(self,num):
        if num==1:
            self.api='https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=c5666fe3ae57bfd62d962baae9080ef55e123fcb'
        if num==2:
            self.api='https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=363139ea2161aff4f4e1a21f58e3928692edde6d'
        else:
            print(f'\033[37;41mHook:error,Please ensure your input\033[0m')
            
    def send(self,text):
        data=('{"content":[{"type":0,"data":"'+text+'"}]}').encode()
        try:
            resp=requests.post(self.api,data)
            print(resp.text)
        except Exception as e:
            print(f'\033[37;41mHook:error[{str(e)}]\033[0m')

