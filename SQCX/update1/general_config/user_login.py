# -*- coding:utf-8 -*-
import web
import json
import hashlib
from rescode import *
from dbconfig import *


class GeneralUserLogin:

    '''用户登录'''
    def OPTIONS(self):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def PUT(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        # token = web.ctx.env.get("HTTP_AUTHORIZATION")
        token = web.cookies().get('general_token')

        # 获取用户输入的用户名，密码
        Data = webinput()
        Username = Data.get('username')
        Password = Data.get('password')
        if Username == '':
            return json.dumps(dict(resCode= Rescode_Username_Cant_Empty, resMsg= Username_Cant_Empty))
        if Password == '':
            return json.dumps(dict(resCode= Rescode_Password_Cant_Empty, resMsg= Password_Cant_Empty))
        # 检验token
        if (token == 'undefined') or (token == None):
            # 没有token，创建新的token
            token = generate_token(Username, 7200)
        else:
            # 有token，检验token是否合法
            Results = certify_token(Username, token)
            if Results == False:
                # 不合法，新建token
                token = generate_token(Username, 7200)

        Data = list(db.select('user', where=dict(name=Username)))
        if not Data:
            return json.dumps(dict(resCode=Rescode_Username_Is_Wrong, resMsg=Username_Is_Wrong))
        # Password_En = Data[0]['password'].encode('utf-8')
        # Password_Md = hashlib.md5(Password_En).hexdigest()
        if Data[0]['password'] != Password:
            return json.dumps(dict(resCode= Rescode_Password_Is_Wrong, resMsg= Password_Is_Wrong))
        else:
            web.setcookie("general_token", token)
            web.setcookie('general_user_name', Username, 7200)
            Org_User = list(db.select('organization_user', where=dict(user_id=Data[0]['id'])))
            if Org_User:
                if len(Org_User) == 1:
                    web.setcookie('general_org_id', Org_User[0]['organization_id'])
                else:
                    web.setcookie('general_org_id', Org_User[1]['organization_id'])
                # web.setcookie('org_name', Org_User[0]['organization_abbreviation_name'], 7200)
            else:
                web.setcookie('general_org_id', None)

                # web.setcookie('general_org_name',None)
            return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))


class GeneralUserLogout:
    def PUT(self):
        web.setcookie('general_user_name','', -1)
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success))

