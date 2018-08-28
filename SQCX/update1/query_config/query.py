#!/usr/bin/evn python
# -*-coding:utf-8 -*-

import urllib
import json
import ssl
import web
from dbconfig import *
from rescode import *


class QueryGuideToaffairs:
    '''办事指南接口'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Query_Org_Id = web.cookies().get('query_org_id')
        Default_Org_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']
        Category_List = list()
        Category_Res = list(db.select('category', where='organization_id=$Query_Org_Id or organization_id=$Default_Org_Id', vars={'Query_Org_Id':Query_Org_Id,'Default_Org_Id':Default_Org_Id}))
        # print Category_Res
        for Category in Category_Res:
            Category_Dict = dict()
            Category_Dict['categoryID'] = Category['category_id']
            Category_Dict['categoryName'] = Category['name']
            Category_Dict['ico'] = Category['ico']
            Category_List.append(Category_Dict)
        data = Category_List
        return json.dumps(dict(resCode=ResCode_Success, resMsg=ResMsg_Success, data=data))


class QueryAffairs:
    '''id,name'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, Category_Id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Category_Msg = list(db.select('category', where=dict(category_id=Category_Id)))
        Sub_Category_Msg = list(db.select('sub_category', where=dict(category_id=Category_Msg[0]['id'])))
        Data = list()
        for Sub_Category in Sub_Category_Msg:
            Sub_Category_Id = Sub_Category['id']
            Business_Msg = list(db.select('business', where=dict(sub_category_id=Sub_Category_Id)))

            Sub_Category_Swap = {}
            for Business in Business_Msg:
                Sub_Category_Swap[Business['id']] = Business['name']
            Sub_Category_Dict = {Sub_Category['name']: Sub_Category_Swap}
            Data.append(Sub_Category_Dict)
        Category_Photo = Category_Msg[0]['photo']
        return json.dumps(dict(resCode=ResCode_Success, resMsg=ResMsg_Success, data=Data, categoryPhoto=Category_Photo))


class QueryDetail:
    '''详细数据'''
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, Business_Id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Business_Msg = list(db.select('business', where=dict(id=Business_Id)))
        Sub_Category_Id = Business_Msg[0]['sub_category_id']
        Sub_Category_Msg = list(db.select('sub_category', where=dict(id=Sub_Category_Id)))
        Sub_Category_Name = Sub_Category_Msg[0]['name']
        Category_Id = Sub_Category_Msg[0]['category_id']
        Category_Msg = list(db.select('category', where=dict(id=Category_Id)))
        Category_Name = Category_Msg[0]['name']
        Org_id = web.cookies().get('query_org_id')
        Data_Dict = dict()
        Data_Dict['enablePrint'] = list(db.select('organization', where=dict(id=Org_id)))[0]['enable_print']
        Data_Dict['category'] = Category_Name
        Data_Dict['name'] = Business_Msg[0]['name']
        Data_Dict['sbbg'] = Business_Msg[0]['sbbg']
        Data_Dict['subCategory'] = Sub_Category_Name
        Data_Dict['id'] = Business_Msg[0]['business_id']
        Data_Dict['crossCity'] = Business_Msg[0]['cross_city']
        Data_Dict['modifiedTime'] = Business_Msg[0]['modified_time']
        Data_Dict['appCondition'] = Business_Msg[0]['app_condition']
        Data_Dict['appMaterial'] = Business_Msg[0]['app_material']
        Data_Dict['operationProcess'] = Business_Msg[0]['operation_process']
        Data_Dict['chargeDesc'] = Business_Msg[0]['charge_desc']
        Data_Dict['policyRef'] = Business_Msg[0]['policy_ref']
        Data_Dict['deptName'] = Business_Msg[0]['dept_name']
        print(Data_Dict)
        return json.dumps(dict(resCode=ResCode_Success, resMsg = ResMsg_Success, data=Data_Dict))

class IndexData:
    def GET(self):
        web.header('content-type', 'text/json')
        org_id = web.cookies().get('query_org_id')
        Org_Data = list(db.select('organization', where=dict(id=org_id)))
        if Org_Data == None:
            return json.dumps(dict(resCode=Rescode_Org_Not_Found, resMsg = Org_Not_Found))
        res_dict = {}
        res_dict['intro'] = Org_Data[0]['intro']
        res_dict['workTime'] = Org_Data[0]['worktime']
        res_dict['phone'] = Org_Data[0]['phone']
        res_dict['traffic'] = Org_Data[0]['traffic']
        res_dict['trafficImage'] = Org_Data[0]['traffic_image']
        res_dict['introImage'] = Org_Data[0]['intro_image']
        res_dict['enablePrint'] = Org_Data[0]['enable_print']
        return json.dumps(dict(resCode=ResCode_Success, resMsg=ResMsg_Success, data=res_dict))


