# -*- coding:utf-8 -*-

import json
import web
from urllib.parse import unquote
import os
from rescode import *
from dbconfig import *


class AdminOrganizationList:
    #机构列表
    def OPTIONS(self):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return
    def GET(self):
        # 获取所有机构列表
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        a = web.ctx
        Results = list(db.select('organization'))
        Data = list()
        if Results != []:
            for i in Results:
                Org = dict()
                Org['orgName'] = i.name
                Org['orgId'] = i.id
                Org['orgIntro'] = i.intro
                Org['orgTraffic'] = i.traffic
                Org['orgWorktime'] = i.worktime
                Org['orgPhone'] = i.phone
                Org['orgTraffic_image'] = i.traffic_image
                Org['orgIntro_image'] = i.intro_image
                Data.append(Org)
            return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success, organizationList=Data))
        return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg=Org_Not_Found))

class AdminOrganization:

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
        # print "111" ,results
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
        Org_Url = Results[0]['org_index_url']
        Enable_Print = Results[0]['enable_print']
        returnData = dict(orgId=Organization_Id, enablePrint=Enable_Print, orgName = Organization_Name,orgIntro=Organization_Intro,orgTraffic=Organization_Traffic,orgWorktime=Organization_Worktime,orgPhone=Organization_Phone,orgTraffic_image=Organization_Traffic_image,orgIntro_image=Organization_Intro_image, orgUrl=Org_Url)
        return json.dumps(returnData)

    def POST(self, org_name):
        ''' 添加新机构'''
        # print ("organization_name:", org_name)
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")

        # 公司简介从传进来的data中获取
        data = web.input()
        org_name = data['orgName']
        org_intro = data['orgIntro']
        org_traffic = data['orgTraffic']
        org_worktime = data['orgWorktime']
        org_phone = data['orgPhone']
        org_url = data["orgUrl"]
        enable_print = data["enablePrint"]
        # org_traffic_image = data['trafficImage']
        # org_intro_image = data['introImage']
        if org_name == '':
            return json.dumps(dict(resCode=Rescode_Org_Name_Cant_Empty, resMsg=Org_Name_Cant_Empty))

            # 判断机构名称是否重复
        Results = list(db.select('organization', where=dict(name=org_name)))
        if Results != []:
            return json.dumps(dict(resCode=Rescode_Org_Name_Cant_Repeat, resMsg=Org_Name_Cant_Repeat))

        if org_intro == "":
             return json.dumps(dict(resCode=Rescode_Org_Intro_Cant_Empty,resMsg=Org_Intro_Cant_Empty))
        if org_traffic == "":
            return json.dumps(dict(resCode=Rescode_Org_Traffic_Cant_Empty,resMsg=Org_Traffic_Cant_Empty))
        if org_worktime == "":
            return json.dumps(dict(resCode=Rescode_Org_Worktime_Cant_Empty ,resMsg=Org_Worktime_Cant_Empty))
        if org_phone == "":
            return json.dumps(dict(resCode=Rescode_Org_Phone_Cant_Empty ,resMsg=Org_Phone_Cant_Empty))

        db.insert('organization', name=org_name, enable_print=enable_print, intro=org_intro,traffic=org_traffic,worktime=org_worktime,phone=org_phone,org_index_url=org_url)
        Results = list(db.select('organization', where=dict(name=org_name)))
        Org_Id = Results[0]['id']
        Org_Name = Results[0]['name']
        Org_Intro = Results[0]['intro']
        Org_Traffic = Results[0]['traffic']
        Org_Worktime = Results[0]['worktime']
        Org_Phone = Results[0]['phone']
        Org_traffic_image = Results[0]['traffic_image']
        Org_intro_image = Results[0]['intro_image']
        Admin_Id = list(db.select('user', where=dict(name='admin'), what='id'))[0]['id']
        db.insert('organization_user', user_id=Admin_Id, organization_id=Org_Id, user_name='admin', organization_name=Org_Name,organization_intro=Org_Intro,organization_phone=Org_Phone,organization_traffic=Org_Traffic,organization_worktime=Org_Worktime,organization_traffic_image=Org_traffic_image,organization_intro_image=Org_intro_image)
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success, orgId=Org_Id))

    def PUT(self, org_id):
        '''修改机构'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        Data = web.input()
        # print data
        if org_id == '':
            return json.dumps(dict(resCode=Rescode_Org_Id_Cant_Empty, resMsg=Org_Id_Cant_Empty))
        try:
            Org_Obj = list(db.select('organization', where=dict(id=org_id)))[0]
            print('_*'*30 , org_id)

            #判断其他条件为空时
            if Data['orgName'] == "":
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
            db.update('organization', where=dict(id=org_id), name=Data['orgName'], intro=Data['orgIntro'],traffic=Data['orgTraffic'],worktime=Data['orgWorktime'],phone=Data['orgPhone'], org_index_url=Data["orgUrl"], enable_print=Data['enablePrint'])
            db.update('organization_user', where=dict(organization_id=org_id), organization_name=Data['orgName'], organization_intro=Data['orgPhone'],
                      organization_traffic=Data['orgTraffic'], organization_worktime=Data['orgWorktime'], organization_phone=Data['orgPhone'])
            return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))
        except IndexError as e:
            return json.dumps(dict(resCode=Org_Not_Found, resMsg=Rescode_Org_Not_Found))

    def DELETE(self, org_id):
        #删除机构
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        print (org_id)
        Results = list(db.select('organization', where=dict(id=org_id)))
        if Results != []:
            db.delete('organization', where=dict(id=org_id))
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))


class AdminCurrentOrganization:
    '''获取当前机构'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, path):
        '''get current organization'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        org_id = web.cookies().get('admin_org_id') #根据名字获取cookie值
        if org_id == 'None':
            Results = list(db.select('organization', where=dict(name=u'默认机构')))
        else:
            Results = list(db.select('organization', where=dict(id=org_id)))
        if Results == []:
            return json.dumps(dict(resCode=Rescode_Cur_Org_Not_Exist, resMsg=Cur_Org_Not_Exist))
        else:
            retData = dict(resCode=Rescode_Success, resMsg=Res_Success,
                            currentOrganizationId=Results[0]['id'],
                            currentOrganization=Results[0]['name'],
                            currentOranizationIntro=Results[0]['intro'],
                            currentOranizationTraffic=Results[0]['traffic'],
                            currentOranizationWorktime=Results[0]['worktime'],
                            currentOranizationPhone=Results[0]['phone'],
                            currentOranizationTraffic_image=Results[0]['traffic_image'],
                            currentOranizationIntro_image=Results[0]['intro_image'])
            web.setcookie('admin_org_id', Results[0]['id'])
            # web.setcookie('admin_org_name', Results[0]['name'])
            return json.dumps(retData)

    def PUT(self, cur_org_id):
        '''change current organization'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        if cur_org_id == '':
            return json.dumps(dict(resCode=Rescode_Cur_Org_Not_Exist, resMsg=Org_Not_Found))
        Results = list(db.select('organization', where=dict(id=cur_org_id)))
        if Results == []:
            return json.dumps(dict(resCode=Rescode_Change_Cur_Org_Error, resMsg=Change_Cur_Org_Error))
        else:
            web.setcookie('admin_org_id', Results[0]['id'])
            # web.setcookie('admin_org_name', Results[0]['name'])
            return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))

#添加机构时的图片上传
class AdminOrganizationPictureUpload:
    #图片上传
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def PUT(self, cur_org_id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = web.input(button_clicked_background_org={}, button_normal_background_org={})
        # print type(id)
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        # print type(id), type(Cur_Org_Id)

        if Cur_Org_Id == '':
            return json.dumps(dict(resCode=Rescode_Cur_Org_Not_Exist, resMsg=Cur_Org_Not_Exist))

        File_Dir = 'static/style/organization_config/' + cur_org_id
        if os.path.exists(File_Dir) == False:
            try:
                os.makedirs(File_Dir)
            except:
                pass

        if 'button_clicked_background_org' in Data:
            # 判断参数的类型是否和dict类型相同
            if not isinstance(Data.button_clicked_background_org, dict):
                if Data.button_clicked_background_org.filename != '':
                    File_Path = Data.button_clicked_background_org.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')

                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_clicked_background_org.file.read())
                        Fout.close()
                        File_Name = '/' + File_Name
                        db.update('organization', where=dict(id=cur_org_id), intro_image=File_Name)
                    except Exception as e:
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e.message))

        if 'button_normal_background_org' in Data:
            if not isinstance(Data.button_normal_background_org, dict):
                if Data.button_normal_background_org.filename != '':
                    File_Path = Data.button_normal_background_org.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')
                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_normal_background_org.file.read())
                        Fout.close()
                        File_Name = '/' + File_Name
                        db.update('organization', where=dict(id=cur_org_id), traffic_image=File_Name)
                    except Exception as e:
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e.message))
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))
