# -*- coding:utf-8 -*-

import json
import os

import web
from rescode import *
from dbconfig import *


class GeneralGetUserBindOrg:
    '''
    获取当前用户下的机构列表,每个用户只能绑定一个机构
    '''

    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self):
        '''
        获取机构用户信息
        '''

        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        User_Name = Data.userName
        Res1 = list(db.select('user', where=dict(name=User_Name)))
        if not Res1:
            return json.dumps(dict(resCode=Rescode_User_Not_Exist, resMsg=User_Not_Exist))
        User_Id = Res1[0]['id']
        # 查询绑定的机构id[]
        Res2 = list(db.select('organization_user', where=dict(user_id=User_Id)))
        Bind_Organization = list()
        for Org in Res2:
            # if len(Res2) > 1:
            Org_Id = Org['organization_id']

            Org_Msg = db.select('organization', where=dict(id=Org_Id))
            if not Org_Msg:
                return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg=Org_Not_Found))
            Org_Name = Org_Msg[0]['name'] #机构的名称
            # Org_Intro = Org_Msg[0]['organization_abbreviation_intro'] #机构的简介
            # Org_Traffic = Org_Msg[0]['organization_abbrevition_traffic'] #机构周围交通
            # Org_Phone = Org_Msg[0]['organization_abbrevition_phone'] #机构联系方式
            # Org_Worktime = Org_Msg[0]['organization_abbrevition_worktime'] #机构工作时间
            # Org_Traffic_image = Org_Msg[0]['organization_abbrevition_traffic_image'] #交通图片
            # Org_Intro_image = Org_Msg[0]['organization_abbrevition_intro_image'] #机构简介图片
            Bind_Organization_Dict = {}
            Bind_Organization_Dict['orgId'] = Org_Id
            Bind_Organization_Dict['orgName'] = Org_Name
            # Bind_Organization_Dict['orgIntro'] = Org_Intro
            # Bind_Organization_Dict['orgTraffic'] = Org_Traffic
            # Bind_Organization_Dict['orgPhone'] = Org_Phone
            # Bind_Organization_Dict['orgWorktime'] = Org_Worktime
            # Bind_Organization_Dict['orgTraffic_image'] = Org_Traffic_image
            # Bind_Organization_Dict['orgIntro_image'] = Org_Intro_image
        Bind_Organization.append(Bind_Organization_Dict)
        retData = dict(resCode=Rescode_Success, resMsg=Res_Success, bindOrganization=Bind_Organization)
        return json.dumps(retData)


#修改机构信息
class GeneralOrganization:
    '''机构增删改查'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, org_id):
        '''获取机构属性'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        if org_id == '':
            return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg=Org_Not_Found))
        Results = list(db.select('organization', where=dict(id=org_id)))
        if Results == []:
            return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg=Org_Not_Found))
        Organization_Id = Results[0]['id']
        Organization_Name = Results[0]['name']
        Organization_Intro = Results[0]['intro']
        Organization_Traffic = Results[0]['traffic']
        Organization_Worktime = Results[0]['worktime']
        Organization_Phone = Results[0]['phone']
        Organization_Traffic_image = Results[0]['traffic_image']
        Organization_Intro_image = Results[0]['intro_image']
        Organization_Enable_Pring = Results[0]['enable_print']
        Organization_Index_Url = Results[0]['org_index_url']
        returnData = dict(orgId=Organization_Id, orgName=Organization_Name, orgIntro=Organization_Intro,
                          orgTraffic=Organization_Traffic, orgWorktime=Organization_Worktime,
                          orgPhone=Organization_Phone, orgTraffic_image=Organization_Traffic_image,
                          orgIntro_image=Organization_Intro_image, enablePrint=Organization_Enable_Pring, orgIndexUrl=Organization_Index_Url)
        return json.dumps(returnData)

    def PUT(self, org_id):
        '''修改机构'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        #print org_id
        Data = web.input()
        #org_name = Data['orgName']
        Org_Obj = list(db.select('organization', where=dict(id=org_id)))
        if not Org_Obj:
            return json.dumps(dict(resCode=Org_Not_Exist, resMsg=Rescode_Org_Not_Found))
        if org_id == '':
            return json.dumps(dict(resCode=Rescode_Org_Id_Cant_Empty, resMsg=Org_Id_Cant_Empty))
        #判断如果为空
        if Data['orgName']=="":
            return json.dumps(dict(resCode=Rescode_Org_Name_Cant_Empty,resMsg=Org_Name_Cant_Empty))
        if Data['orgIntro'] == "":
            return json.dumps(dict(resCode=Rescode_Org_Intro_Cant_Empty, resMsg=Org_Intro_Cant_Empty))
        if Data['orgTraffic'] == "":
            return json.dumps(dict(resCode=Rescode_Org_Traffic_Cant_Empty, resMsg=Org_Traffic_Cant_Empty))
        if Data['orgWorktime'] == "":
            return json.dumps(dict(resCode=Rescode_Org_Worktime_Cant_Empty, resMsg=Org_Worktime_Cant_Empty))
        if Data['orgPhone'] == "":
            return json.dumps(dict(resCode=Rescode_Org_Phone_Cant_Empty, resMsg=Org_Phone_Cant_Empty))

        # edit organization
        db.update('organization', where=dict(id=org_id), name=Data['orgName'], intro=Data['orgIntro'],
                      traffic=Data['orgTraffic'], worktime=Data['orgWorktime'], phone=Data['orgPhone'], enable_print=Data['enablePrint'], org_index_url=Data['orgIndexUrl'])
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))

    def DELETE(self, org_id):
        # 删除机构
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Results = list(db.select('organization', where=dict(id=org_id)))
        if Results != []:
            db.delete('organization', where=dict(id=org_id))
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))

#图片上传
class GeneralOrganizationPictureUpload:
    #图片上传
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def PUT(self, org_id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")

        Data = web.input(button_clicked_background_gen={}, button_normal_background_gen={})
        # print '111', Data

        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        if Cur_Org_Id == '':
            return json.dumps(dict(resCode=Rescode_Cur_Org_Not_Exist, resMsg=Cur_Org_Not_Exist))

        File_Dir = 'static/style/organization_config/' + org_id
        if os.path.exists(File_Dir) == False:
            try:
                os.makedirs(File_Dir)
            except:
                pass

        if 'button_clicked_background_gen' in Data:  #intro图片
            if  not isinstance(Data.button_clicked_background_gen, dict):
                # print '1111', Data.button_clicked_background.filename
                if Data.button_clicked_background_gen.filename != '':
                    File_Path = Data.button_clicked_background_gen.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    print (File_Name , type(File_Name))
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')
                    # print '2122', File_Name
                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_clicked_background_gen.file.read())
                        Fout.close()
                        File_Name = '/' + File_Name
                        db.update('organization', where=dict(id=org_id ), intro_image=File_Name)
                    except Exception as e:
                        print(e)
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e.message))

        if 'button_normal_background_gen' in Data:
            # traffic_image
            if  not isinstance(Data.button_normal_background_gen,dict):
                if Data.button_normal_background_gen.filename != '':
                    File_Path = Data.button_normal_background_gen.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')
                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_normal_background_gen.file.read())
                        Fout.close()
                        db.update('organization', where=dict(id=org_id), traffic_image='/' + File_Name)
                    except Exception as e:
                        print(e)
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e.message))

        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))


