#!/usr/bin/evn python
# -*-coding:utf-8 -*-

import urllib2
import urllib
import json
import web

url = (
    '/(.*)/', 'redirect',
    '(.*\..{1,4})','StaticFile',
    '/', 'Index',
    '/init', 'Init',
    '/guide_to_affairs', 'Guide_to_affairs',
    '/affairs/(.*)','Affairs',
    '/detail/(.*)','Detail',
    '/refresh', 'refresh')

class redirect:
    '''URL不区分大小写、URL可加或不加/结尾'''
    def GET(self, path):
        print("path: ", path)
        return web.seeother('/'+path.lower())

    def POST(self, path):
        return web.seeother('/'+path.lower())

    def PUT(self, path):
        return web.seeother('/'+path.lower())

    def DELETE(self, path):
        return web.seeother('/'+path.lower())

class StaticFile:
    '''提供web服务'''
    def GET(self, file):
        web.seeother('/static'+file)      #重定向

class Index:
    '''主页路由'''
    def GET(self):
        return web.seeother('/index.html')

class refresh:
    def GET(self):
        return web.seeother('/refresh.html')

Rescode_Success = 1001
Resmsg_Success = u'success'
Rescode_Please_Refresh_Data = 1002
Resmsg_Please_Refresh_Data = u'请刷新初始数据'


def get_token():
    # 请求令牌
    request = urllib2.Request('https://oauth.shwsq.cn/token')
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    params = {"grant_type": "client_credentials", "client_id": "781214c6c6f0471e96c313665a0d7159",
              "client_secret": "rdxn3ds#p9"}
    params = urllib.urlencode(params)
    response = urllib2.urlopen(request, params)
    msg = response.read()
    msg = json.loads(msg)
    # print("token return:", msg)
    token = msg['access_token']
    return token


def category_data(token):
    category_data = dict()
    # token = get_token()
    token = token

    # 请求id，name
    auth = 'bearer ' + token
    request_header = {"Authorization": auth}
    request = urllib2.Request('https://sqggfw.shwsq.cn/api/affairitem/categorylist', headers=request_header)
    request.headers = request_header
    # request.add_header("Authorization", str(auth))	这样添加的Authorization会被capitalize
    response = urllib2.urlopen(request)
    msg2 = response.read()
    msg2 = json.loads(msg2)
    # print msg2

    bycategory_list = list()
    for i in msg2:
        id = i['CategoryID']
        # # 请求信息
        request = urllib2.Request('https://sqggfw.shwsq.cn/api/affairitem/bycategory/' + str(id))
        request.add_header("Authorization", "bearer " + token)
        response = urllib2.urlopen(request)
        msg3 = response.read()
        msg3 = json.loads(msg3)
        bycategory_list.append(msg3)

    category_data['categorylist'] = msg2
    category_data['bycategory'] = bycategory_list
    return category_data


token = '\-hKMhh0bRPUuJ5pDutwPv7m8hafZ2oSZzuxHMG40zWD5Z4rEkiUQ42NYhG9Fc3vv4xHwrNxZSNTS_oHtFIdKJcR_LmxvV31svNec778jAMlFerV_XrxzKj115pcH1YX4cTh_kn7p__5y6o'
token = 'BaAjFvy6WeW9FsCBYSMo0lUdjfpfcGeaK9ifM1X-mqT9hdP2XCPAZfetnuP0DLMf6N9tWtd3IBTw9czTvzDA-HngCctg8WsORbXe_2C4fSEgHJrGyKE5ISkZMXnfHJVGg3GMqEPWzdjnxWRHFo7MmGunnXfMu8_l8wLSt1fNS7tNjqSKDHzx09yGbTwpmtr5rPRIiskX2-xm-44RIBV_9f33jq-tnyQ69aPMTikfGJnOZitk38o3-psCNDN2-cCqk1uGqBfqf1tjlwn2B4MH4TFo1mKUOuFuO5u-UhqscxMU8TAbFRwiC0iCGbY'


class Init:
    '''初始化接口'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Refresh_Data.refresh_data()
        return json.dumps(dict(Rescode=Rescode_Success, Resmsg=Resmsg_Success))

class Guide_to_affairs:
    '''办事指南接口'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        try:
            data = category['categorylist']
            return json.dumps(dict(Rescode=Rescode_Success, Resmsg = Resmsg_Success, Data=data))
        except:
            return json.dumps(dict(Rescode=Rescode_Please_Refresh_Data, Resmsg=Resmsg_Please_Refresh_Data))

class Affairs:
    '''id,name'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, category_name):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        sub_name_list = list()
        for bycategory in category['bycategory']:
            for object in bycategory:
                cate_gory = object['Category']
                if cate_gory != category_name:
                    continue
                if cate_gory == category_name:
                    sub_name_list.append(object['SubCategory'])
        sub_name_list = set(sub_name_list)
        data = []
        for sub_name in sub_name_list:
            name_list = list()
            #print("sub_name:", sub_name)
            #print("type(sub_name):", type(sub_name))
            sub_dict = {}
            if sub_name is None:
                sub_dict = {category_name : name_list}
            else:
                sub_dict = {sub_name : name_list}

            for bycategory in category['bycategory']:
                for object in bycategory:
                    if object['SubCategory'] is None:
                        if object['Category'] == category_name:
                            name_list.append(object['Name'])
                    else:
                        if object['SubCategory'] == sub_name:
                            name_list.append(object['Name'])
            data.append(sub_dict)
        return json.dumps(dict(Rescode=Rescode_Success, Resmsg = Resmsg_Success, Data=data))



class Detail:
    '''详细数据'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, name):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        data = ''
        for bycategory in category['bycategory']:
            for i in bycategory:
                if i['Name'] == name:
                    data = i
        return json.dumps(dict(Rescode=Rescode_Success, Resmsg = Resmsg_Success, Data=data))

class Refresh_Data:
    '''初始化接口'''
    category = ''
    token = ''
    def __init__(self):
        self.refresh_data()

    def refresh_data(self):
        try:
            self.category = category_data(self.token)
        except urllib2.HTTPError, e:
            print e.message
            self.token = get_token()
            print('****************************token: ', self.token)
            self.category = category_data(self.token)
        global category
        global token
        category = self.category
        token = self.token

app = web.application(url, globals())
Refresh_Data = Refresh_Data()
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()

