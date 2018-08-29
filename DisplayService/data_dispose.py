# -*- encoding:utf-8 -*-
from threading import Thread

from settings import Display_Service_Config, Singleton
from sooket_send import UdpSend
from call_type_mapping import Evt58_Screen_Need_Fields
from serial_port_send import SerialPortCommunication


@Singleton
class DisposeData:

    def __str__(self):
        return '数据处理类'

    def make_threading(self, func, *args):
        '''
        创建线程
        :param func: 线程执行的函数
        :param args: 执行函数需要的参数
        :return: 线程对象
        '''
        course = Thread(target=func, args=args)
        return course

    def dispose(self, Data, client):
        '''
        :param Data: 后台转发数据
        :param client: sooket对象
        :return: None
        '''
        print('接收到后台服务转发请求: ', Data)
        Request_Type = int(Data['type'])
        WinNumber = Data.get('winNumber')
        Res = {}
        try:
            Res = Display_Service_Config['window'][WinNumber]
        except KeyError as e:
            print('该窗口处于未配置显示服务')
        if Res:
            # 获取窗口屏幕类型
            if Res.get('windowScreenType') == 5:
                # Vsd异步屏窗口类型
                Ip = Res.get('windowScreenIp'), '704'

                # 发送消息
                udpSend= UdpSend(Ip, Data, client)
                course = self.make_threading(udpSend.course_vsd_screen)
                course.start()
                course.join()

            else:
                try:
                    # EVT58窗口屏幕
                    Res_EVT_Dict = {}
                    for item in Evt58_Screen_Need_Fields:
                        Res_EVT_Dict[item] = Res[item]
                    window = Display_Service_Config['window_info']
                    Type = Data['type']
                    WinNumber = Data['winNumber']
                    ComName = Res_EVT_Dict['comName']
                    BpsRate = Res_EVT_Dict.get('bpsRate')
                    TicketNumber = Data.get('ticketNumber')
                    TicketShow = Res_EVT_Dict['ticketShow']
                    evt58ChipAddr = Res_EVT_Dict['evt58ChipAddr']
                    businessShow = Res_EVT_Dict['businessShow']
                    window['businessShow'] = businessShow

                    # 发送消息
                    SerialPort = SerialPortCommunication()
                    self.coures_evt = self.make_threading(SerialPort.course_send_mag_evt,
                                                          Type,
                                                          WinNumber,
                                                          ComName,
                                                          BpsRate,
                                                          TicketNumber,
                                                          TicketShow,
                                                          evt58ChipAddr,
                                                          businessShow)
                    self.coures_evt.start()
                    self.coures_evt.join()
                except KeyError as e:
                    print('未找到该窗口显示设备配置, 请确保该窗口设备配置完成', e)

            if Request_Type == 1:
                # 请求类型为1的时候需要通知综合屏,其余状态不通知
                Mscreen_List = Res.get('windowMscreen')
                if Mscreen_List:
                    Ip = Mscreen_List[0].get('msip'), Mscreen_List[0].get('msport')
                    udpSend = UdpSend(Ip, Data, client)
                    course = self.make_threading(udpSend.threading_high_definition_screen)
                    course.start()
                    course.join()

                # 获取LED综合屏
                if 'windowLEDMscreen' in Res:
                    Led_Dict = Res.get('windowLEDMscreen')[0]
                    BpsRate = Res.get('bpsRate')
                    ledAddr = Led_Dict['ledAddr']
                    TicketNumber = Data.get('ticketNumber')
                    ledScreenComName = Led_Dict['ledScreenComName']
                    ledTemplateShowContent = Led_Dict['ledTemplateShowContent']
                    SerialPort = SerialPortCommunication()
                    self.course_led = self.make_threading(SerialPort.course_send_led_screen,
                                                          BpsRate,
                                                          ledAddr,
                                                          WinNumber,
                                                          TicketNumber,
                                                          ledScreenComName,
                                                          ledTemplateShowContent)
                    self.course_led.start()
                    self.course_led.join()

