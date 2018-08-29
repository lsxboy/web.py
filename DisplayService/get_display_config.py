# -*- encoding:UTF-8 -*-
import configparser
import time
import os

import requests

from settings import Display_Service_Config, config_file_name, Api_Path, Singleton
from call_type_mapping import Need_Data

@Singleton
class ScreenConfig:

    def __str__(self):
        return '改类主要获取显示服务的主要配置, 并将其保存至Settings.py中的 Display_Service_Config字典中'

    def local_config(self):
        # 读取后台配置
        # Ip_List = socket.gethostbyname_ex(socket.gethostname())[2]    # 获取本机IP地址信息
        Config = configparser.ConfigParser()
        Dir = os.getcwd() + config_file_name

        try:
            Config.read(Dir)
            # 获取所有参数，返回一个元组
            Get = Config.get
            return Get('paramert', 'ip'), Get('paramert', 'host'), Get('paramert', 'organizationId')
        except configparser.NoSectionError as e:
            raise FileExistsError('配置文件出错，请重新配置', e)

    def get_display_config(self, Par_Tuple):
        # 获取后台ip地址，拼接url
        url = f'http://{Par_Tuple[0]}:{Par_Tuple[1]}{Api_Path}{Par_Tuple[2]}'
        Res = requests.get(url)

        while True:
            if Res.status_code == requests.codes.ok:
                Res.encoding = 'utf-8'
                Python_Obj = Res.json()
                swap = {}
                Window_Diaplay_Content = {}
                if Python_Obj['resCode'] == 0 and Python_Obj['displayService'] != []:
                    Display_Obj = Python_Obj['displayService'][0]
                    Display_Service_Config['Ip'] = (Display_Obj['displayServiceIp'], Display_Obj['displayServicePort'])

                    # 循环将所有json数据获取
                    for item in Need_Data:
                        if item == 'window':
                            window = Display_Obj[item]
                            for index in range(len(window)):
                                win = window[index]    # 直接将json整个窗口数据保存
                                swap[win['windowName']] = win    # 键为窗口号, 值为改窗口的json
                            Display_Service_Config['window'] = swap
                        else:
                            Window_Diaplay_Content[item] = Display_Obj[item]
                    Display_Service_Config['window_info'] = Window_Diaplay_Content
                    return Display_Service_Config['Ip']
                else:
                    print('后台配置的地址或者参数有误, 或者未开启窗口服务, 请配置后, 重新启动!')
                    return False
            else:
                print('请求错误，请检查后台服务是否启动，5秒后重新尝试获取！')
                time.sleep(5)


















