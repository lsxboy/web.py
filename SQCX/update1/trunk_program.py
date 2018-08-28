#!/usr/bin/evn python
# -*-coding:utf-8 -*-

import web
import hashlib
from dbconfig import *

from admin_config.business_config import *
from admin_config.category_config import *
from admin_config.org_config import *
from admin_config.refurbish import *
from admin_config.sub_category_config import *
from admin_config.user import *

from general_config.business_config import *
from general_config.category_config import *
from general_config.org_config import *
from general_config.sub_category_config import *
from general_config.user_login import *

from query_config.query import *
url = (
    '/(.*)/', 'redirect',
    '(.*\..{1,4})','StaticFile',
    '/admin', 'AdminIndex',
    '/general', 'GeneralIndex',
    '/query/(\d+)', 'QueryIndex',
    '/admin/init', 'AdminInit',
    '/admin/user_login', 'AdminUserLogin',
    '/admin/logout', 'AdminUserLogout',
    '/admin/user/(.*)', 'AdminUser',
    '/admin/user_list', 'AdminUserList',
    '/admin/organization/(.*)', 'AdminOrganization',
    '/admin/org_list', 'AdminOrganizationList',   #机构列表路由
    '/admin/current_organization/(.*)', 'AdminCurrentOrganization',
    '/admin/category/(.*)', 'AdminCategoryConfig',
    '/admin/category_list', 'AdminCategoryList',
    '/admin/sub_category/(.*)', 'AdminSubCategoryConfig',
    '/admin/sub_category_list/(.*)', 'AdminSubCategoryList',
    '/admin/business/(.*)', 'AdminBusinessConfig',
    '/admin/business_list/(.*)', 'AdminBusinessList',
    '/admin/category_picture_upload/(.*)', 'AdminCategoryPictureUpload',
    '/admin/organization_picture_upload/(.*)','AdminOrganizationPictureUpload',#admin添加机构时的图片

    '/general/user_login', 'GeneralUserLogin',
    '/general/logout', 'GeneralUserLogout',
    '/general/get_user_bind_org', 'GeneralGetUserBindOrg',
    '/general/category/(.*)', 'GeneralCategoryConfig',
    '/general/category_list', 'GeneralCategoryList',
    '/general/organization/(.*)','GeneralOrganization',  #加载机构详情
    '/general/organization_picture_upload/(.*)','GeneralOrganizationPictureUpload',#用户对图片的修改
    '/general/category_picture_upload/(.*)', 'GeneralCategoryPictureUpload',
    '/general/sub_category/(.*)', 'GeneralSubCategoryConfig',
    '/general/sub_category_list/(.*)', 'GeneralSubCategoryList',
    '/general/business/(.*)', 'GeneralBusinessConfig',
    '/general/business_list/(.*)', 'GeneralBusinessList',

    '/query/guide_to_affairs', 'QueryGuideToaffairs',
    '/query/affairs/(.*)','QueryAffairs',
    '/query/detail/(.*)','QueryDetail',

    '/index_data', 'IndexData',
)

class redirect:
    '''URL不区分大小写、URL可加或不加/结尾'''
    def GET(self, path):
        print("path: ", path)
        return web.seeother('/'+path.lower())

    def POST(self, path):
        return web.seeother('/'+path.lower())

    def PUT(self, path):
        return web.seeother('/'+path.lower())

    def DELETE(self, path):
        return web.seeother('/'+path.lower())

class StaticFile:
    '''提供web服务'''
    def GET(self, file):
        web.seeother('/static'+file)      #重定向

class AdminIndex:
    '''主页路由'''
    def GET(self):
        return web.seeother('/admin_static/admin_index.html')

class GeneralIndex:
    '''主页路由'''
    def GET(self):
        return web.seeother('/general_static/new_index.html')

class QueryIndex:
    '''主页路由'''
    def GET(self, org_id):
        web.setcookie('query_org_id', org_id)
        print('-------------------测试机构', org_id )
        Org_Data = list(db.select('organization', where=dict(id=org_id)))
        print ('-*' * 30, Org_Data)
        return web.seeother(Org_Data[0]["org_index_url"])


app = web.application(url, globals())

if __name__ == "__main__":
    #根据表user 查询名字为admin的用户  转换成列表
    Has_Admin = list(db.select('user', where=dict(name='admin')))
    #根据机构表，查询默认机构
    Default_Org = list(db.select('organization', where=dict(name='默认机构')))
    #机构和用户
    Admin_Org = list(db.select('organization_user', where=dict(user_name='admin', organization_name='默认机构')))
    if not Has_Admin:
        #如果管理员不存在，加入admin用户
        Password_En = u'lonzon'.encode('utf-8')
        Password_Md = hashlib.md5(Password_En).hexdigest()
        db.insert('user', name="admin",password=Password_Md)
    if not Default_Org:
        #如果默认机构不存在，加加一个默认机构
        db.insert('organization', name='默认机构')
        Default_Org = list(db.select('organization', where=dict(name='默认机构')))
    if not Admin_Org:
        db.insert('organization_user',
                  organization_id=Default_Org[0]['id'], #默认机构的id
                  organization_name=Default_Org[0]['name'], #默认机构的名字
                  user_id=Has_Admin[0]['id'], #管理员用户id
                  user_name=Has_Admin[0]['name']) #管理员用户名字
    app.run()

