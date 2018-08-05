#!/usr/bin/env python3
#接收线程和发送线程类

import threading
from OpenSSL import SSL

#接收线程
class RecThread(threading.Thread):
    def __init__(self,s,ip,conn):
        threading.Thread.__init__(self)
        self.__s=s
        self.__ip=ip
        self.__conn = conn
    def run(self):
        lock=threading.Lock()
        while 1:
            try:
                msg = self.__conn.recv(1024)    #接收
                lock.acquire()  #锁定屏幕
                print(self.__ip+':'+msg.decode('utf-8'))    #打印消息到屏幕
                lock.release()  #释放锁
            except SSL.Error:
                print(self.__ip+'已断开.')
                break
        self.__s.close()

#发送线程
class SendThread(threading.Thread):
    def __init__(self,s,ip,conn):
        threading.Thread.__init__(self)
        self.__s=s
        self.__ip=ip
        self.__conn = conn
    def run(self):
        lock=threading.Lock
        while 1:
            msg=input()
            try:
                self.__conn.send(msg.encode('utf-8'))   #发送
            except SSL.Error:
                print(self.__ip + '已断开.')
                break
        self.__s.close()