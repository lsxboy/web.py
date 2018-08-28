import time
import hashlib
from urllib.parse import urlencode
import requests


def sendmessage(phone,auth):
    #请求地址
    post_url  ='   https://api.miaodiyun.com/20150822/industrySMS/sendSMS'
    #请求头
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    #用户Sid
    accountSid = "f7f6532f13574c18ae5e6709a2552d6e"
    #token值
    auth_token = '145f48d9f9ef47e4a69cd8c0173af2e0'
    #时间戳
    timestamp = time.strftime("%Y%m%d%H%M%S")
    #sig
    sig = accountSid + auth_token + timestamp
    #md5加密
    md = hashlib.md5()
    md.update(sig.encode('utf-8'))
    #16进制的
    sig = md.hexdigest()
    #模板参数
    yzm = str(auth)
    t = '5'
    param = yzm +','+ t
    form_data = {
        'accountSid':accountSid,
        'timestamp':timestamp,
        'templateid':'194713666',
        'to':phone,
        'sig':sig,
        'param':param,
    }
    #将字典转换为url参数
    form_data = urlencode(form_data)
    requests.post(url=post_url,data=form_data,headers=headers)

