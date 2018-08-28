#!/usr/bin/evn python
# -*-coding:utf-8 -*-

# import urllib
from urllib import request
import json
import ssl
import web
from dbconfig import db
from rescode import *

# def get_token():
#     # 请求令牌
#     request = urllib2.Request('https://oauth.shwsq.cn/token')
#     # {"error":"invalid_grant","error_description":"The clientID or clientSecret is incorrect."}
#     # 设置Jquery的Ajax请求默认方式,这种方式的好处就是浏览器都支持
#     request.add_header("Content-Type", "application/x-www-form-urlencoded")
#     # grant_type：设置授权模式 客户端证书。id.密码
#     params = {"grant_type": "client_credentials", "client_id": "781214c6c6f0471e96c313665a0d7159",
#               "client_secret": "rdxn3ds#p9"}
#     params = urllib.urlencode(params)
#     response = urllib2.urlopen(request, params)
#     msg = response.read()
#     msg = json.loads(msg)
#     # print("token return:", msg)
#     token = msg['access_token']
#     return token



def get_token():
    url = r'http://www.baidu.com'
    headers = {
        "Content-Type": r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
        "grant_type": "client_credentials",
        "client_id": "781214c6c6f0471e96c313665a0d7159",
        "client_secret": "rdxn3ds#p9"
    }
    request = urllib.request.Request(url=url, headers=headers)
    content = urllib.request.urlopen(request).read().decode()
    return content




def category_data(token):
    # 请求数据
    category_data = dict()
    # token = get_token()
    token = token

    # 请求id，name
    auth = 'bearer ' + token
    # 通过令牌获取信息
    request_header = {"Authorization": auth}
    request = urllib2.Request('https://sqggfw.shwsq.cn/api/affairitem/categorylist', headers=request_header)
    request.headers = request_header
    # request.add_header("Authorization", str(auth))	这样添加的Authorization会被capitalize（利用）
    # 设置全局取消证书验证
    # ssl._create_default_https_context = ssl._create_unverified_context
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
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


# token = '\-hKMhh0bRPUuJ5pDutwPv7m8hafZ2oSZzuxHMG40zWD5Z4rEkiUQ42NYhG9Fc3vv4xHwrNxZSNTS_oHtFIdKJcR_LmxvV31svNec778jAMlFerV_XrxzKj115pcH1YX4cTh_kn7p__5y6o'
token = 'WQJJGnRGQ8AD-kJbHx9eYCE1jbBm5fAMV3yLtgVZlb7fz55VofEmw-FYFIXL1E87ZHwITx3vEmfM37tS48m0sT6AfwvhvbluFfYdnr2xQBWoPMkXhKU4mNrHrOmCxS_ZKZGOm7ojneA7m0kiaiDvxBI-4Tltybh1wK1Jw6U-iHBKwP6Va9rzyEIRTc83hZrlwEm4XFF-zoG9R087N6CH-eKxydCTLuTFe7-9SKj_eZ1OyZYPoR-aANJRmpw9jbZw1EFnb_vu9m1Moh33Ri6nFdHGsX-rm_tbEAUrzlIu3CGfxBRyFXTedFulUpI'
class AdminInit:
    '''初始化接口'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        global category
        global token
        try:
            category = category_data(token)
        except urllib2.HTTPError as e:
            print (e.message)
            token = get_token()
            print('****************************token: ', token)
            category = category_data(token)

        Organization_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']

        for category_list in category['categorylist']:
            Res = list(db.select('category', where=dict(organization_id=Organization_Id, category_id=category_list['CategoryID'], name=category_list['CategoryName'])))
            if not Res:
                # 添加大类id，name到数据库
                db.insert('category', organization_id=Organization_Id, category_id=category_list['CategoryID'], name=category_list['CategoryName'],is_change=0)
                Res = list(db.select('category',where=dict(organization_id=Organization_Id, category_id=category_list['CategoryID'],
                                                           name=category_list['CategoryName'])))
            for by_category in category['bycategory']:
                if by_category[0]['Category'] == category_list['CategoryName']:
                    for sub_category in by_category:
                        if sub_category['SubCategory'] == None:
                            sub_category['SubCategory'] = category_list['CategoryName']
                        Res2 = list(db.select('sub_category',where=dict(category_id=Res[0]['id'],
                                                                        name=sub_category['SubCategory'])))
                        if not Res2:
                            # 添加小类名字到数据库
                            db.insert('sub_category',category_id=Res[0]['id'], name=sub_category['SubCategory'])
                            Res2 = list(db.select('sub_category',
                                                  where=dict(category_id=Res[0]['id'],name=sub_category['SubCategory'])))
                        Res3 = list(db.select('business', where=dict(sub_category_id=Res2[0]['id'], business_id = sub_category['ID'])))
                        if not Res3:
                            db.insert('business',
                                      sub_category_id=Res2[0]['id'],
                                      business_id = sub_category['ID'],
                                      name=sub_category['Name'],
                                      dept_name =sub_category['DeptName'],
                                      policy_ref=sub_category['PolicyRef'],
                                      app_condition=sub_category['AppCondition'],
                                      app_material=sub_category['AppMaterial'],
                                      operation_process=sub_category['OperationProcess'],
                                      charge_desc = sub_category['ChargeDesc'],
                                      cross_city=sub_category['CrossCity'],
                                      modified_time = sub_category['ModifiedTime'],
                                      sbbg = sub_category['SBBG'])
        return json.dumps(dict(resCode=ResCode_Success, resMsg=ResMsg_Success))