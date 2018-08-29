# -*- encoding:utf-8 -*-
from settings import Display_Service_Config, Dll, Singleton
from call_type_mapping import Call_Type_Map

@Singleton
class SerialPortCommunication:

    def __str__(self):
        return '串口通信类, 主要用与EVT窗口屏, LED综合屏的通信'

    def open_serial_port(self, Com_Name, BpsRate):
        '''
        该函数功能为打开串口
        :param Com_Name: 串口的名字
        :param BpsRate: 比特率
        :return: 返回打开的串口号
        '''
        Com_Name = 'COM' + str(Com_Name)
        return Dll.portOpen(Com_Name.encode(), int(BpsRate), 'n', 8, 1)

    def course_send_led_screen(self, BpsRate, Led_Addr, WinNumber, TicketNumber, ledScreenComName, ledTemplateShowContent):
        '''
        LED屏发送函数
        :param BpsRate: 比特率
        :param Led_Addr: LED综合屏地址
        :param WinNumber: 窗口号码
        :param TicketNumber: 票号码
        :param ledScreenComName: LED屏串口号
        :param ledTemplateShowContent: LED屏配置的显示格式
        :return: None
        '''
        New_Content = str(ledTemplateShowContent).replace('%t', str(TicketNumber)).replace('%w', str(WinNumber))
        ledScreenComName = 'COM' + str(ledScreenComName)
        HandleNumber = Dll.portOpen(ledScreenComName.encode(), BpsRate, 'n', 8, 1)
        Res = Dll.picSend(HandleNumber, Led_Addr, 2, New_Content.encode('gbk'), '0x11')
        Dll.portClose(HandleNumber)
        if Res:
            print('LED综合屏发送失败', HandleNumber, Led_Addr, New_Content)
        else:
            print('LED综合屏发送成功', Res)

    def course_send_mag_evt(self, Type, WinNumber, ComName, BpsRate, TicketNumber, TicketShow, evt58ChipAddr, businessShow):
        '''
        EVT屏发送函数
        :param Type: 呼叫器的呼叫的类型
        :param WinNumber: 窗口号码
        :param ComName: 串口号
        :param BpsRate: 比特率
        :param TicketNumber: 票号码
        :param TicketShow: 呼叫票时窗口屏幕显示格式
        :param evt58ChipAddr: 窗口屏地址
        :param businessShow: 该窗口的受理业务
        :return: None
        '''
        led_handle = self.open_serial_port(ComName, BpsRate)
        if led_handle:
            windo_data = Display_Service_Config['window_info']    # 该数据是窗口屏幕显示需要的字段
            Base_Content = windo_data[Call_Type_Map[Type]]    # 使用字典映射, 传给字典呼叫的类型,返回相应的字段

            # 准备发送内容, 并且需要替换显示内容
            Full_Content = ''

            if Type == 1:
                Full_Content = TicketShow.replace('%t', TicketNumber)
            elif Type == 3:
                Full_Content = Base_Content.replace('%t', TicketNumber)
            else:
                Full_Content = Base_Content
            # 发送
            ResNumber = Dll.dataSend(led_handle, evt58ChipAddr, Full_Content.encode('gbk'), '0x11', 0, 1, 10)
            Dll.portClose(led_handle)
            if ResNumber:
                print('EVT窗口屏消息发送失败: ', led_handle, evt58ChipAddr, Full_Content)
            else:
                print('EVT窗口屏消息发送成功: ', Full_Content)
        else:
            print('EVT窗口屏打开失败, 串口未打开', led_handle)

    def init_window(self):
        '''
        启动程序时, 初始化所有窗口屏
        :return: None
        '''
        Windows = Display_Service_Config['window']
        screenPauseService = Display_Service_Config['window_info']['screenPauseService']

        for window_index in Windows:
            evt58ChipAddr = Windows[window_index].get('evt58ChipAddr')
            BpsRate = Windows[window_index].get('bpsRate')
            Com_Name = 'COM' + str(Windows[window_index].get('comName'))
            showMethod = Windows[window_index].get('showMethod')
            showSpeed = Windows[window_index].get('showSpeed')
            waitTime = Windows[window_index].get('waitTime')
            if evt58ChipAddr:
                Led_Handle = Dll.portOpen(Com_Name.encode(), int(BpsRate), 'n', 8, 1)
                if Led_Handle:
                    Res = Dll.dataSend(Led_Handle, evt58ChipAddr, screenPauseService.encode('gbk'), '0x11', showMethod, showSpeed, waitTime)
                    Dll.portClose(Led_Handle)
                    if Res:
                        print('初始化窗口消息发送失败', Led_Handle, evt58ChipAddr, screenPauseService)
                    else:
                        print('初始化窗口消息发送成功', screenPauseService)
                else:
                    # Dll.portClose(Led_Handle)
                    print('初始化窗口失败, 串口未打开:', Led_Handle)