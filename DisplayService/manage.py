# -*- encoding:utf8 -*-
import socket

from get_display_config import ScreenConfig
from data_dispose import DisposeData
from settings import Q
from serial_port_send import SerialPortCommunication


class Main:
    def __str__(self):
        return '该类为启动类, 获取配置, 监听, 并调用数据处理类进行处理'

    def __init__(self):
        self.screen = ScreenConfig()
        self.Back_Ip = self.screen.local_config()
        self.Ip_Post = self.screen.get_display_config(self.Back_Ip)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self):
        if not self.Ip_Post:
            return False
        print(f'正在监听端口:', self.Ip_Post)
        self.client.bind(self.Ip_Post)

        # 初始化窗口屏
        Display_Obj = DisposeData()
        SerialPort_Obj = SerialPortCommunication()
        course = Display_Obj.make_threading(SerialPort_Obj.init_window())
        course.start()
        course.join()

        # 进入循环监听
        while True:
            Base_Data, Address = self.client.recvfrom(512)
            Encoding_Data = (eval(Base_Data.decode(encoding='utf-8')))
            if Encoding_Data['type'] == 9:
                self.reboot()

            elif Encoding_Data['type'] == 10:
                Q.put({'ACK': True})    # ACK:对收到的数据包进行的确认
                print('将ACK值推送到队列中')

            else:
                disp = DisposeData()
                disp.dispose(Encoding_Data, self.client)

    def reboot(self):
        print('正在重新应用配置')
        self.client.close()
        self.__init__()
        self.listen()


if __name__ == '__main__':
    main = Main()
    main.listen()











