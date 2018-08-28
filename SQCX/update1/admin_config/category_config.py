#!/usr/bin/evn python
# -*-coding:utf-8 -*-

from dbconfig import *
from rescode import *
import os


class AdminCategoryList:
    '''    '''
    def OPTIONS(self):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return
    def GET(self):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        # Default_Org_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']
        # if int(Cur_Org_Id) == int(Default_Org_Id):
        #     Category_List = list(db.select('category'))
        # else:
        #     Category_List = list(db.select('category', where='organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id', vars={'Cur_Org_Id':Cur_Org_Id, 'Default_Org_Id':Default_Org_Id}))
        Category_List = list(db.select('category', where=dict(organization_id = Cur_Org_Id)))
        Category_Data_List = list()
        for Category in Category_List:
            Category_Dict = dict()
            Category_Dict['id'] = Category['id']
            Category_Dict['name'] = Category['name']
            Category_Dict['isChange'] = Category['is_change']
            Category_Data_List.append(Category_Dict)
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, Data=Category_Data_List))


class AdminCategoryConfig:
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def GET(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        Category_Msg = list(db.select('category', where=dict(organization_id=Cur_Org_Id,id=id)))
        if Category_Msg:
            Category_Dict = dict()
            Category_Dict['id'] = Category_Msg[0]['id']
            Category_Dict['categoryId'] = Category_Msg[0]['category_id']
            Category_Dict['name'] = Category_Msg[0]['name']
            Category_Dict['ico'] = Category_Msg[0]['ico']
            Category_Dict['photo'] = Category_Msg[0]['photo']
            Category_Dict['isChange'] = Category_Msg[0]['is_change']
        # else:
        #     Category_Msg = list(db.select('category', where=dict(organization_id=0, id=id)))
        #     if Category_Msg:
        #         Category_Dict = dict()
        #         Category_Dict['id'] = Category_Msg[0]['id']
        #         Category_Dict['categoryId'] = Category_Msg[0]['category_id']
        #         Category_Dict['name'] = Category_Msg[0]['name']
        #         Category_Dict['ico'] = Category_Msg[0]['ico']
        #         Category_Dict['photo'] = Category_Msg[0]['photo']
        #         Category_Dict['isChange'] = Category_Msg[0]['is_change']
        else:
            return jsondumps(dict(resCode=Rescode_Category_Is_Inexistence, resMsg=Category_Is_Inexistence))
        return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, Data=Category_Dict))

    def POST(self, path):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        Default_Org_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']
        if Data['categoryId'] and Data['name']:
            Category_Id = Data['categoryId']
            Name = Data['name']
            Res = list(db.select('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and category_id=$Category_Id',vars={'Cur_Org_Id':Cur_Org_Id,'Default_Org_Id':Default_Org_Id,'Category_Id':Category_Id}))
            if Res:
                return jsondumps(dict(resCode=Rescode_Category_Id_Cant_Repeat, resMsg=Category_Id_Cant_Repeat))
            Res = list(db.select('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and name=$Name',vars={'Cur_Org_Id':Cur_Org_Id,'Default_Org_Id':Default_Org_Id,'Name':Name}))
            if Res:
                return jsondumps(dict(resCode=Rescode_Category_Name_Cant_Repeat, resMsg=Category_Name_Cant_Repeat))

            print('---------------------------------------------', Cur_Org_Id, Default_Org_Id)
            if int(Cur_Org_Id) == int(Default_Org_Id):
                db.insert('category', organization_id=Cur_Org_Id, category_id=Category_Id, name=Name, is_change=0)
            else:
                db.insert('category', organization_id=Cur_Org_Id, category_id=Category_Id, name=Name, is_change=1)
            Res = list(db.select('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and name=$Name',vars={'Cur_Org_Id':Cur_Org_Id,'Default_Org_Id':Default_Org_Id,'Name':Name}))
            if Res:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success, id=Res[0]['id']))
        else:
            return jsondumps(dict(resCode=Rescode_Category_Id_Or_Name_Cant_Empty, resMsg=Category_Id_Or_Name_Cant_Empty))

    def PUT(self, id):
        '''保存'''
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = webinput()
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        Default_Org_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']
        if Data['categoryId'] and Data['name']:
            Category_Id = Data['categoryId']
            Name = Data['name']
            db.update('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and id=$id', category_id=Category_Id, name=Name, vars={'Default_Org_Id':Default_Org_Id, 'Cur_Org_Id':Cur_Org_Id, 'id':id})
            # Res = list(db.select('category', where=dict(organization_id=Cur_Org_Id, id=id, category_id=Category_Id, name=Name)))
            Res = list(db.select('category',
                                 where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and id=$id and category_id=$Category_Id and name=$Name',
                                 vars={'Default_Org_Id':Default_Org_Id,'Cur_Org_Id':Cur_Org_Id, 'id':id, 'Category_Id':Category_Id, 'Name':Name}))
            if Res:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success,id=Res[0]['id']))
        else:
            return jsondumps(dict(resCode=Rescode_Category_Id_Or_Name_Cant_Empty, resMsg=Category_Id_Or_Name_Cant_Empty))

    def DELETE(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        Default_Org_Id = list(db.select('organization', where=dict(name='默认机构')))[0]['id']
        Res = list(db.select('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and id=$id', vars={'Default_Org_Id':Default_Org_Id,'Cur_Org_Id':Cur_Org_Id, 'id':id}))
        if Res:
            db.delete('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and id=$id', vars={'Default_Org_Id':Default_Org_Id,'Cur_Org_Id':Cur_Org_Id, 'id':id})
            Res2 = list(db.select('category', where='(organization_id=$Cur_Org_Id or organization_id=$Default_Org_Id) and id=$id', vars={'Default_Org_Id':Default_Org_Id,'Cur_Org_Id':Cur_Org_Id, 'id':id}))
            if Res2:
                return jsondumps(dict(resCode=Rescode_Delete_Error, resMsg=Delete_Error))
            else:
                return jsondumps(dict(resCode=Rescode_Success, resMsg=Res_Success))
        else:
            return jsondumps(dict(resCode=Rescode_Category_Is_Inexistence, resMsg=Category_Is_Inexistence))

# 图片的保存
class AdminCategoryPictureUpload:
    def OPTIONS(self, path):
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Origin", "*")
        return

    def PUT(self, id):
        web.header('content-type', 'text/json')
        web.header("Access-Control-Allow-Origin", "*")
        Data = web.input(button_clicked_background={}, button_normal_background={})
        Cur_Org_Id = web.ctx.env.get('HTTP_ADMIN_ORG_ID')
        if Cur_Org_Id == '':
            return json.dumps(dict(resCode=Rescode_Cur_Org_Not_Exist, resMsg=Cur_Org_Not_Exist))

        File_Dir = 'static/style/category_config/' + id
        if os.path.exists(File_Dir) == False:
            try:
                os.makedirs(File_Dir)
            except:
                pass

        if 'button_clicked_background' in Data:
            if not isinstance(Data.button_clicked_background, dict):
                # print '1111', Data.button_clicked_background.filename
                if Data.button_clicked_background.filename != '':
                    File_Path = Data.button_clicked_background.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')
                    # print '2122', File_Name
                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_clicked_background.file.read())
                        Fout.close()
                        File_Name = '/' + File_Name
                        db.update('category', where='(organization_id=$Cur_Org_Id or organization_id=0) and id=$id', ico=File_Name, vars={'Cur_Org_Id': Cur_Org_Id, 'id': id})
                    except Exception as e:
                        print(e)
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e))

        if 'button_normal_background' in Data:
            if not isinstance(Data.button_normal_background, dict):
                if Data.button_normal_background.filename != '':
                    File_Path = Data.button_normal_background.filename.replace('\\', '/')
                    File_Name = File_Path.split('/')
                    if ' ' in File_Name:
                        File_Name = File_Name.replace(' ', '')
                    File_Name = File_Dir + '/' + File_Name[0]
                    Fout = open(File_Name, 'wb')
                    try:
                        Fout.write(Data.button_normal_background.file.read())
                        Fout.close()
                        db.update('category', where='(organization_id=$Cur_Org_Id or organization_id=0) and id=$id', photo='/' + File_Name, vars={'Cur_Org_Id': Cur_Org_Id, 'id': id})
                    except Exception as e:
                        print(e)
                        return json.dumps(dict(resCode=Rescode_Error, resMsg=e))
        return json.dumps(dict(resCode=Rescode_Success, resMsg=Res_Success))