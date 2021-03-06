#!/usr/bin/env python3

from OpenSSL import SSL
import socket
import sys,argparse
import Thread

KEYFILE='client.key'
CERTFILE='client.crt'
CAFILE='ca.crt'

def verify_cb(conn, cert, errnum, depth, ok):
    print('取得证书: %s' % cert.get_subject())
    return ok

#解析命令行
parser=argparse.ArgumentParser(usage='\n ./%(prog)s -d ip -p port',conflict_handler='resolve')
parser.add_argument('-d','--destination',type=str,help='目标ip')
parser.add_argument('-p','--port',type=str,help='目标端口')
args=parser.parse_args(sys.argv[1:])
ip=args.destination
port=args.port

#初始化context
context=SSL.Context(SSL.SSLv23_METHOD)
context.set_options(SSL.OP_NO_SSLv2)
context.set_options(SSL.OP_NO_SSLv3)
context.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT,verify_cb)
context.use_privatekey_file(KEYFILE)
context.use_certificate_file(CERTFILE)
context.load_verify_locations(CAFILE)

#开启服务
s=SSL.Connection(context,socket.socket(socket.AF_INET,socket.SOCK_STREAM))
s.connect((ip,int(port)))

#创建接收线程
recThread=Thread.RecThread(s,ip)
#创建发送线程
sendThread=Thread.SendThread(s,ip)
#开启线程
recThread.start()
sendThread.start()



