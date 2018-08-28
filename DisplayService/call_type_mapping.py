
Evt58_Screen_Need_Fields = [
    'evt58ChipAddr',
    'businessShow',
    'showMethod',
    'windowShow',
    'ticketShow',
    'showSpeed',
    'waitTime',
    'comName',
    'bpsRate',
]

# 需要在json数据中获取的字段,后台所有数据分为8个字段
Need_Data = [
        'vsvsdIpList',
        'screenRestoreService',
        'screenDefaultShow',
        'screenPauseService',
        'screenHandleShow',
        'displayServiceIp',
        'displayServicePort',
        'window'
]

# 根据呼叫类型, 向窗口屏展示不同的内容
Call_Type_Map = {
    1: 'screenPauseService',
    3: 'screenHandleShow',
    4: 'businessShow',
    5: 'screenPauseService',
    6: 'businessShow',
    7: 'businessShow',
    8: 'screenPauseService'
}

# 呼叫类型对象操作
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
'''