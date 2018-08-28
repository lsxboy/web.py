# -*- coding:utf-8 -*-
'''
/******************************************************************************
*main.cpp		: web service constant explain
*Company		: lonzon
*Author 		：WangZhonghua
*Date			: 2017-08-20
*Last Modify	: 2017-09-04
******************************************************************************/
'''

import web
import json
import urllib
import time
import base64
import random

Rescode_Success = 0
Res_Success = "Success"
Rescode_Error = u'发生错误'
ResCode_Success = 1001
ResMsg_Success = u'success'


Rescode_Save_Db_Error = 1101
Save_Db_Error = u'保存数据库失败'
Rescode_Delete_Error = 1102
Delete_Error = u'删除失败'

Rescode_Org_Name_Cant_Empty = 1001
Org_Name_Cant_Empty = u"机构名称不能为空"
Rescode_Org_Id_Cant_Empty = 1002
Org_Id_Cant_Empty = u"机构id不能为空"
Rescode_Org_Name_Cant_Repeat = 1003
Org_Name_Cant_Repeat = u"机构名称不能重复"


Rescode_Org_Intro_Cant_Empty = 1004
Org_Intro_Cant_Empty = u"机构简介不能为空"
Rescode_Org_Traffic_Cant_Empty = 1005
Org_Traffic_Cant_Empty = u"周边交通不能为空"
Rescode_Org_Worktime_Cant_Empty = 1007
Org_Worktime_Cant_Empty = u"工作时间详情不能为空"
Rescode_Org_Phone_Cant_Empty = 10011
Org_Phone_Cant_Empty = u"联系方式不能为空"


Rescode_Org_Not_Found = 1006
Org_Not_Found = u'机构未找到'
Rescode_Org_Not_Exist = 1008
Org_Not_Exist = u'机构不存在'
Rescode_Change_Cur_Org_Error = 1009
Change_Cur_Org_Error = u'修改当前机构失败'
Rescode_Cur_Org_Not_Exist = 1010
Cur_Org_Not_Exist = u'未配置当前机构'

Rescode_Category_Id_Cant_Repeat = 2001
Category_Id_Cant_Repeat = u'大类类别id不能重复'
Rescode_Category_Name_Cant_Repeat = 2002
Category_Name_Cant_Repeat = u'大类类别名称不能重复'
Rescode_Category_Id_Or_Name_Cant_Empty = 2003
Category_Id_Or_Name_Cant_Empty = u'大类类别id，名称均不能为空'
Rescode_Category_Is_Inexistence = 2004
Category_Is_Inexistence = u'大类类别不存在'
Rescode_Category_Not_Sub = 2005
Category_Not_Sub = u'大类下没有小类'

Rescode_Sub_Category_Cant_Repeat = 3001
Sub_Category_Cant_Repeat = u'小类不能重复'
Rescode_Sub_Category_Cant_Empty = 3002
Sub_Category_Cant_Empty = u'小类信息不能为空'
Rescode_Sub_Category_Is_Inexistence = 3003
Sub_Category_Is_Inexistence = u'小类类别不存在'

Rescode_Business_Id_Cant_Repeat = 4001
Business_Id_Cant_Repeat = u'业务id不能重复'
Rescode_Business_Name_Cant_Repeat = 4002
Business_Name_Cant_Repeat = u'业务名称不能重复'
Rescode_Business_Is_Inexistence = 4003
Business_Is_Inexistence = u'业务不存在'

# 登陆
Rescode_Username_Cant_Empty = 5001
Username_Cant_Empty = u"用户名不能为空"
Rescode_Password_Cant_Empty = 5002
Password_Cant_Empty = u"密码不能为空"
Rescode_Password_Is_Wrong = 5003
Password_Is_Wrong = u"密码错误"
Rescode_Username_Is_Wrong = 5004
Username_Is_Wrong = u"用户名不存在"
Rescode_Old_Password_Cant_Empty = 5005
Old_Password_Cant_Empty = u"旧密码不能为空"
Rescode_New_Password_Cant_Empty = 5006
New_Password_Cant_Empty = u"新密码不能为空"
Rescode_Sure_Password_Cant_Empty = 5007
Sure_Password_Cant_Empty = u"确认密码不能为空"
Rescode_Two_Password_Not_Equal = 5008
Two_Password_Not_Equal = u'两次密码不相同'
Rescode_Old_Password_Error = 5009
Old_Password_Error = u'原密码错误'

# user 用户
Rescode_User_Not_Exist = 6001
User_Not_Exist = u"用户不存在"
Rescode_Bind_Organization_Cant_Empty = 6002,
Bind_Organization_Cant_Empty = u"绑定机构不能为空"
Rescode_User_Save_Fail = 6003
User_Save_Fail = u"用户信息保存失败"
Rescode_User_Is_Exist = 6004
User_Is_Exist = u'用户已存在'
Rescode_User_Msg_Not_Null = 6005
User_Msg_Not_Null = u'用户不能为空值'
Rescode_User_Del_Error = 6006
User_Del_Error = u'用户删除失败'


def webinput():
    '''判断请求头和实际请求参数格式'''
    Data = ''
    if web.ctx.env.get('REQUEST_METHOD') == 'GET':
        Data = web.input()
    else:
        try:
            Data = json.loads(web.data())   #尝试先以json格式解析
        except:
            Data = urllib.unquote(web.data()) #Json解析不对，直接以键值对格式解析
            Data = dict((l.split('=') for l in Data.split('&')))
    return Data


def jsondumps(data):
    return json.dumps(data, ensure_ascii=False)

def generate_token(key, expire):
    # 创建token
    Bg_Ts = time.time()
    Ov_Ts = str(Bg_Ts + expire)
    Token_String = str(str(Bg_Ts) +"_" +str(random.random()) +"_" +str(key) +"_" +Ov_Ts)
    Token = base64.encodestring(Token_String)
    B64_Token = base64.urlsafe_b64encode(Token.encode("utf-8"))
    return B64_Token

def certify_token(key, token):
    # 验证token
    Token = base64.urlsafe_b64decode(token).decode('utf-8')
    Token_String = base64.decodestring(Token)
    Token_List = Token_String.split('_')
    if len(Token_List) != 4:
        return False
    Ts_Str = Token_List[3]
    if float(Ts_Str) < time.time():
        return False
    Username = Token_List[2]
    if str(key) != Username:
        print(key, Username)
        return False
    return True