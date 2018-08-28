# -*-coding:utf-8 -*-
from rescode import *
from dbconfig import *



class AdminBusinessList:

    def OPTIONS(self, path):
        '''
       所支持的请求方法
       '''
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, sub_category_id):
        '''
        根据子组id返回信息
        '''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Business_Msg = list(db.select('business', where=dict(sub_category_id=sub_category_id)))
        Business_List = list()
        for Business in Business_Msg:
            Business_Dict = dict()
            Business_Dict['id'] = Business['id']
            Business_Dict['name'] = Business['name']
            Business_List.append(Business_Dict)
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, businessList=Business_List))


class AdminBusinessConfig:

    def OPTIONS(self, path):
        '''
       所支持的请求方法
       '''
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return
    def GET(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Business_Msg = list(db.select('business', where=dict(id=id)))
        # Business_List = list()
        if Business_Msg:
            Business_Dict = dict()
            # Business_Dict['crossCity'] = Business_Msg[0]['cross_city']
            # Business_Dict['modifiedTime'] = Business_Msg[0]['modified_time']
            Business_Dict['appCondition'] = Business_Msg[0]['app_condition']
            Business_Dict['appMaterial'] = Business_Msg[0]['app_material']
            Business_Dict['operationProcess'] = Business_Msg[0]['operation_process']
            Business_Dict['chargeDesc'] = Business_Msg[0]['charge_desc']
            Business_Dict['policyRef'] = Business_Msg[0]['policy_ref']
            # Business_Dict['sbbg'] = Business_Msg[0]['sbbg']
            Business_Dict['deptName'] = Business_Msg[0]['dept_name']
            Business_Dict['businessId'] = Business_Msg[0]['business_id']
            Business_Dict['name'] = Business_Msg[0]['name']
            # Business_List.append(Business_Dict)
            return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, businessData=Business_Dict))

    def POST(self, path):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Business_Id = Data['businessId']
        Business_Name = Data['name']
        Sub_Category_Id = Data['subCategoryId']
        Res = list(db.select('business', where=dict(sub_category_id = Sub_Category_Id, business_id=Business_Id)))
        if Res:
            return jsondumps(dict(resCode=Rescode_Business_Id_Cant_Repeat, resMsg=Business_Id_Cant_Repeat))
        Res2 = list(db.select('business', where=dict(name=Business_Name)))
        if Res2:
            return jsondumps(dict(resCode=Rescode_Business_Name_Cant_Repeat, resMsg=Business_Name_Cant_Repeat))
        db.insert('business',
                  # organization_id=Cur_Org_Id,
                  sub_category_id=Sub_Category_Id,
                  business_id=Business_Id,
                  name=Business_Name,
                  dept_name=Data['deptName'],
                  policy_ref=Data['policyRef'],
                  app_condition=Data['appCondition'],
                  app_material=Data['appMaterial'],
                  operation_process=Data['operationProcess'],
                  charge_desc=Data['chargeDesc'],
                  # cross_city=Data['crossCity'],
                  # modified_time=Data['modifiedTime'],
                  # sbbg=Data['SBBG']
                  )
        Res = list(db.select('business', where=dict(business_id=Business_Id, name=Business_Name, sub_category_id=Sub_Category_Id)))
        if Res:
            return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, id=Res[0]['id']))

    def PUT(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Business_Id = Data['businessId']
        Business_Name = Data['name']
        Sub_Category_Id = Data['subCategoryId']
        Res = list(db.select('business', where=dict(sub_category_id=Sub_Category_Id, business_id=Business_Id)))
        if Res:
            return jsondumps(dict(resCode=Rescode_Business_Id_Cant_Repeat, resMsg=Business_Id_Cant_Repeat))
        Res2 = list(db.select('business', where=dict(name=Business_Name)))
        if Res2:
            return jsondumps(dict(resCode=Rescode_Business_Name_Cant_Repeat, resMsg=Business_Name_Cant_Repeat))
        db.update('business', where=dict(id=id),
                  sub_category_id=Sub_Category_Id,
                  business_id=Business_Id,
                  name=Business_Name,
                  dept_name=Data['deptName'],
                  policy_ref=Data['policyRef'],
                  app_condition=Data['appCondition'],
                  app_material=Data['appMaterial'],
                  operation_process=Data['operationProcess'],
                  charge_desc=Data['chargeDesc'],
                  # cross_city=Data['crossCity'],
                  # modified_time=Data['modifiedTime'],
                  # sbbg=Data['SBBG']
                  )
        Res = list(db.select('business',
                             where=dict(business_id=Business_Id, name=Business_Name, sub_category_id=Sub_Category_Id)))
        if Res:
            return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, id=Res[0]['id']))

    def DELETE(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Res = list(db.select('business', where=dict(id=id)))
        if Res:
            db.delete('business', where=dict(id=id))
            Res2 = list(db.select('business', where=dict(id=id)))
            if Res2:
                return jsondumps(dict(resCode=Rescode_Delete_Error, resMsg=Delete_Error))
            else:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success))
        else:
            return jsondumps(dict(resCode=Rescode_Business_Is_Inexistence, resMsg=Business_Is_Inexistence))