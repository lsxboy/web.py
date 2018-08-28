# -*- coding:utf-8 -*-

from django.conf.urls import url
from axf import views

urlpatterns = [

    url(r'^$', views.index),



    url(r'^home/$',views.home),
    url(r'^market/(\w+)/(\w+)/(\w+)/$',views.market),
    url(r'^cart/$',views.cart),

    url(r'^mine/$',views.mine),
    #登陆界面
    url(r'^login/$', views.login),
    url(r'^quit/$', views.quit),

    #显示详情
    url(r"^market/(\w+)/(\w+)/(\w+)/(\w+)/$",views.xiangqing),

    #显示收货地址
    url(r'^dizhi/$', views.dizhi),
    #添加收货地址
    url(r'^add/$', views.add),
    #更新收货地址
    url(r'^update/$', views.update),

    #更改购物车
    url(r'^changecart/$', views.changecart),
    url(r'^changecart2/(\w+)/$', views.changecart2),
    url(r"^changecart/(\w+)/$", views.changecart),


    #账号注册
    url(r"^register/$",views.register),
    #用户详情
    url(r"^particulars/$",views.particulars),

    # 序列化用户
    url(r'^userlist/$', views.userlist),
    url(r'^userlist/(?P<pk>\d+)$', views.users),

    #订单查询
    url(r'^order_form/$', views.order_form),
]