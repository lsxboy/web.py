# -*- coding:utf-8 -*-
import web
import pymysql

db_type = 'mysql'
db_username = 'root'
db_port = 3306
db_name = 'sqcx'
db_password = 'lsxboy'
db_host = "localhost"

db = web.database(dbn=db_type, user=db_username, pw=db_password, db=db_name, host=db_host, port=db_port)

# db = pymysql.connect(host='local', port=3306, user='root', passwd='lsxboy', db='sqcx')
