# -*- encoding:utf-8 -*-
import json

from settings import *


class UdpSend:

    def __init__(self, Ip, Content, Client):
        '''
        :param Ip: UDP发送目标的Ip
        :param Content: 要发送的内容
        :param Client: sooket对象
        '''
        self.Ip = Ip
        self.Content = Content
        self.Client = Client

    def __str__(self):
        return 'UDP通信类'

    def threading_high_definition_screen(self):
        self.Client.sendto(json.dumps(self.Content).encode('utf-8'), self.Ip)
        try:
            Res = Q.get(timeout=3)['ACK']
            print('收到高清综合屏回包', Res)
        except queue.Empty as e:
            print('3秒钟内未收到高清综合屏回包', e)

    def course_vsd_screen(self):
        self.Client.sendto(json.dumps(self.Content).encode('utf-8'), self.Ip)
        try:
            Res = Q.get(timeout=3)['ACK']
            print('收到VSD异步屏回包', Res)
        except queue.Empty as e:
            print('3秒钟内未收到VSD异步屏回包', e)
