# -*- coding:utf-8 -*-
import web
import json
import hashlib
from rescode import *
from dbconfig import *


class AdminUserList:
    def GET(self):
        # 获取所有用户列表
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Results = list(db.select('user'))
        Data = list()
        if Results != []:
            for i in Results:
                User_Dict = dict()
                User_Dict['userId'] = i.id
                User_Dict['username'] = i.name
                Data.append(User_Dict)
            return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, userList=Data))
        return jsondumps(dict(resCode=Rescode_User_Not_Exist, resMsg=User_Not_Exist))


class AdminUserLogin:
    '''用户登录'''
    def OPTIONS(self):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def PUT(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        token = web.ctx.env.get("HTTP_AUTHORIZATION")

        # 获取用户输入的用户名，密码
        Data = webinput()
        Username = Data.get('username')
        Password = Data.get('password')
        if Username == '':
            return json.dumps(dict(resCode= Rescode_Username_Cant_Empty, resMsg= Username_Cant_Empty))
        if Password == '':
            return json.dumps(dict(resCode= Rescode_Password_Cant_Empty, resMsg= Password_Cant_Empty))
        # 检验token
        if token == 'undefined' or token == None:
            # 没有token，创建新的token
            token = generate_token(Username, 7200)
        else:
            # 有token，检验token是否合法
            Results = certify_token(Username, token)
            if Results == False:
                # 不合法，新建token
                token = generate_token(Username, 7200)

        Data = list(db.select('user', where= dict(name = Username)))
        if not Data:
            return json.dumps(dict(resCode=Rescode_Username_Is_Wrong, resMsg=Username_Is_Wrong))
        # Password_En = Data[0]['password'].encode('utf-8')
        # Password_Md = hashlib.md5(Password_En).hexdigest()
        if Data[0]['password'] != Password:
            return json.dumps(dict(resCode= Rescode_Password_Is_Wrong, resMsg= Password_Is_Wrong))
        else:
            web.setcookie("admin_token", token)
            web.setcookie('admin_user_name', Username, 7200)
            Org_User = list(db.select('organization_user',where=dict(user_id=Data[0]['id'])))
            if Org_User:
                web.setcookie('admin_org_id', Org_User[0]['organization_id'])
                # web.setcookie('org_name', Org_User[0]['organization_abbreviation_name'], 7200)
            else:
                web.setcookie('admin_org_id', None)
                # web.setcookie('org_name',None)
            return json.dumps(dict(resCode= Rescode_Success, resMsg= Res_Success))


class AdminUserLogout:

    def PUT(self):
        web.setcookie('user_name', '', -1)
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success))


class AdminUser():

    def OPTIONS(self,path):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, id):
        '''获取用户属性'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Res1 = list(db.select('user', where=dict(id=id)))
        if Res1 == []:
            return json.dumps(dict(resCode=Rescode_User_Not_Exist, resMsg=User_Not_Exist))
        User_Id = Res1[0]['id']
        Res2 = list(db.select('organization_user', where=dict(user_id=User_Id)))
        Org_Id_List = list()
        Bind_Organization = list()
        for Org in Res2:
            Org_Id = Org['organization_id']
            Org_Msg = db.select('organization', where=dict(id=Org_Id))
            if not Org_Msg:
                return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg=Org_Not_Found))
            Org_Name = Org_Msg[0]['name']
            Bind_Organization_Dict = {}
            Bind_Organization_Dict['orgId'] = Org_Id
            Bind_Organization_Dict['orgName'] = Org_Name
            Bind_Organization.append(Bind_Organization_Dict)
        ret_Data = dict(
            resCode=Rescode_Success, resMsg=Res_Success, username=Res1[0]['name'],
            password=Res1[0]['password'],
            bindOrganization=Bind_Organization
        )
        return json.dumps(ret_Data)

    def POST(self,path):
        '''添加用户'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        if Data['username'] == '':
            return json.dumps(dict(resCode=Rescode_Username_Cant_Empty, resMsg=Username_Cant_Empty))
        if Data['password'] == '':
            return json.dumps(dict(resCode=Rescode_Password_Cant_Empty, resMsg=Password_Cant_Empty))
        if Data['bindOrganization'] == '':
            return json.dumps(dict(resCode=Rescode_Bind_Organization_Cant_Empty, resMsg=Bind_Organization_Cant_Empty))
        Bind_Organization_Dict = json.loads(Data['bindOrganization'])
        User_Msg = db.select('user', where=dict(name=Data['username']))
        if User_Msg:
            return jsondumps(dict(resCode = Rescode_User_Is_Exist, resMsg=User_Is_Exist))
        Password = Data['password']
        Password_En = Password.encode('utf-8')
        Password_Md = hashlib.md5(Password_En).hexdigest()
        db.insert('user', name=Data['username'], password=Password_Md)
        Results = list(db.select('user', where=dict(name = Data['username'])))
        if Results == []:
            return json.dumps(dict(resCode=Rescode_User_Save_Fail, resMsg=User_Save_Fail))
        User_Id = Results[0]['id']
        username = Results[0]['name']
        for i in Bind_Organization_Dict:
            if Bind_Organization_Dict[i] == True:
                db.insert('organization_user', user_id = User_Id, user_name = username, organization_id=i)
        return json.dumps(dict(resCode = Rescode_Success, resMsg = Res_Success))

    def PUT(self, id):
        '''修改用户信息'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        Username = Data['username']
        Password = Data['password']
        Bind_Organization_Dict = json.loads(Data['bindOrganization'])
        if not Username:
            return json.dumps(dict(resCode= Rescode_Username_Cant_Empty, resMsg= Username_Cant_Empty))
        if not Password:
            return json.dumps(dict(resCode=Rescode_Password_Cant_Empty, resMsg=Password_Cant_Empty))
        User_Msg = list(db.select('user', where=dict(id=id)))
        if User_Msg == []:
            return json.dumps(dict(resCode=Rescode_User_Not_Exist, resMsg=User_Not_Exist))
        User_Id = User_Msg[0]['id']
        User_Password = User_Msg[0]['password']
        if Password != User_Password:
            Password_En = Password.encode('utf-8')
            Password = hashlib.md5(Password_En).hexdigest()
        db.update('user',where = dict(id = User_Id), name = Username, password = Password)
        New_Org_Id_List = list()
        for i in Bind_Organization_Dict:
            if Bind_Organization_Dict[i] == True:
                Org_Id = i
                New_Org_Id_List.append(Org_Id)
        # 查询修改前的user_organization表格里的数据
        Org_Msg = list(db.select('organization_user', where=dict(user_id=User_Id)))
        Old_Org_Id_List = list()
        for Old_Org_Dict in Org_Msg:
            Old_Org_Id_List.append(Old_Org_Dict['organization_id'])
        for i in Old_Org_Id_List:
            if i in New_Org_Id_List:
                pass
            if i not in New_Org_Id_List:
                db.delete('organization_user', where=dict(user_id=User_Id, organization_id=i))
        for i in New_Org_Id_List:
            if i in Old_Org_Id_List:
                pass
            if i not in Old_Org_Id_List:
                db.insert('organization_user', user_id=User_Id, organization_id=i)
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))

    def DELETE(self, id):
        '''删除用户'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        Res = db.select('user', where =dict(id = id))
        if Res == '':
            return json.dumps(dict(resCode = Rescode_User_Not_Exist, resMsg = User_Not_Exist))
        db.delete('user', where =dict(id = id))
        Res = db.select('user', where =dict(id = id))
        if Res:
            return jsondumps(dict(resCode= Rescode_User_Del_Error, resMsg= User_Del_Error))
        return json.dumps(dict(resCode =Rescode_Success, resMsg =Res_Success))
