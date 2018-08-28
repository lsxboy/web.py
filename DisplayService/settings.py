# -*- encoding:utf-8 -*-
import queue
import os
import ctypes

# 队列存放ACK状态, 用与查看综合屏是否收到信息, 是对收到的数据包确认.
Q = queue.Queue()

# 配置文件
config_file_name = '\static\lzqs.ini'

# 存放显示服务配置列表
Display_Service_Config = dict()

# dlltpzp.dll 为C++编写的动态库, Python调用需要用到ctypes标准库中的WinDLL将其打开,
# 并得到一个对象, 可使用改对象中的函数方法进行与窗口屏进行通信, Word文档请参考蓝宗开发资料.
File_Name = 'static\dlltpzp.dll'
Now_PATH = os.path.dirname(__file__)
DllPath = os.path.join(Now_PATH, File_Name)
Dll = ctypes.WinDLL(DllPath)

# API接口路径
Api_Path = '/back/org_display_service_config/'

# 后台服务请求类型映射.
'''
1：叫号重呼，
3: 开始办理，
4：结束业务，
5：暂停服务，
6：恢复服务，
7：登录，
8：退出，
9：重启
10：屏幕向发送者发送确认包

# 屏幕类型映射
5: 高清综合屏
6: LEd综合屏
4: VSD异步屏
7: 5字8字EVT模版
'''



