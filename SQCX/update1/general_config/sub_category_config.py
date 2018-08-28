from rescode import *
from dbconfig import *

class GeneralSubCategoryList:
    def GET(self, category_id):
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        # Category_Msg = list(db.select('category', where=dict(name=category_name)))
        # Category_Id = Category_Msg[0]['id']
        Sub_Category_Msg = list(db.select('sub_category', where=dict(category_id=category_id)))
        if Sub_Category_Msg:
            Sub_Category_List = list()
            for Sub_Category in Sub_Category_Msg:
                Sub_Category_Dict = dict()
                Sub_Category_Dict['id'] = Sub_Category['id']
                Sub_Category_Dict['name'] = Sub_Category['name']
                Sub_Category_List.append(Sub_Category_Dict)
            return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, subCategoryList=Sub_Category_List))
        return jsondumps(dict(resCode=Rescode_Category_Not_Sub, resMsg=Category_Not_Sub))


class GeneralSubCategoryConfig:
    def GET(self, sub_category_id):
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Sub_Category_Msg = list(db.select('sub_category', where=dict(id=sub_category_id)))
        Sub_Category_Dict = dict()
        if Sub_Category_Msg:
            Sub_Category_Dict['sub_category_id'] = Sub_Category_Msg[0]['id']
            Sub_Category_Dict['sub_category_name'] = Sub_Category_Msg[0]['name']
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, Data=Sub_Category_Dict))

    def POST(self,path):
        Data = webinput()
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        # Cur_Org_Id = 1
        if Data['name'] and Data['categoryId']:
            Sub_Category_Name = Data['name']
            Category_Id = Data['categoryId']
            Res = list(db.select('sub_category', where=dict(category_id=Category_Id, name=Sub_Category_Name)))
            if Res:
                return jsondumps(dict(resCode=Rescode_Sub_Category_Cant_Repeat, resMsg=Sub_Category_Cant_Repeat))
            db.insert('sub_category', category_id=Category_Id, name=Sub_Category_Name)
            Res = list(db.select('sub_category', where=dict(category_id=Category_Id, name=Sub_Category_Name)))
            if Res:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, subCategoryId=Res[0]['id']))
        else:
            return jsondumps(dict(resCode=Rescode_Sub_Category_Cant_Empty, resMsg=Sub_Category_Cant_Empty))

    def PUT(self, sub_category_id):
        Data = webinput()
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        if Data['name'] and Data['categoryId']:
            Sub_Category_Name = Data['name']
            Category_Id = Data['categoryId']
            Res = list(db.select('sub_category', where=dict(category_id=Category_Id, name=Sub_Category_Name)))
            if Res:
                return jsondumps(dict(resCode=Rescode_Sub_Category_Cant_Repeat, resMsg=Sub_Category_Cant_Repeat))
            db.update('sub_category', where=dict(id=sub_category_id), category_id=Category_Id, name=Sub_Category_Name)
            Res = list(db.select('sub_category', where=dict(category_id=Category_Id, name=Sub_Category_Name)))
            if Res:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, subCategoryId=Res[0]['id']))
        else:
            return jsondumps(dict(resCode=Rescode_Sub_Category_Cant_Empty, resMsg=Sub_Category_Cant_Empty))

    def DELETE(self, sub_category_id):
        # Cur_Org_Id = web.ctx.env.get('HTTP_ORG_ID')
        Res = list(db.select('sub_category', where=dict(id=sub_category_id)))
        if Res:
            db.delete('sub_category', where=dict(id=sub_category_id))
            Res2 = list(db.select('sub_category', where=dict(id=sub_category_id)))
            if Res2:
                return jsondumps(dict(resCode=Rescode_Delete_Error, resMsg=Delete_Error))
            else:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success))
        else:
            return jsondumps(dict(resCode=Rescode_Sub_Category_Is_Inexistence, resMsg=Sub_Category_Is_Inexistence))


