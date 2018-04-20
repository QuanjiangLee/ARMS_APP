#! /usr/bin/python3
#-*-coding:utf-8-*-
import select
import hashlib
import struct
import time
from mylog import xtrace, SOCKET_IN, SOCKET_OUT
from db_operate import check_user_name, check_user_passwd
NO_SPECIFIC = 'Unknown'
HEAD_FORMAT = "!3sI"
HEAD_SIZE = struct.calcsize(HEAD_FORMAT)

def send_info(sock, kind, info, user_no=NO_SPECIFIC):
    xtrace("%s [%s] %s %s" % (SOCKET_OUT, user_no, kind, info))
    buf = info.encode()
    rest_size = len(buf)
    buf = struct.pack(HEAD_FORMAT, kind.encode(), rest_size) + buf
    ret = 0
    try:
        ret = sock.send(buf)
    except Exception:
        ret = -1
    return ret > 0

# 向客户端发送命令执行结果
def reply_client(sock, status, user_no=None):
    if sock is None:
        return False

    if user_no is not None:
        xtrace("%s [%s] %s" % (SOCKET_OUT, user_no, status))

    confirm = status.encode()
    rest_pkt_size = len(confirm)
    buf = struct.pack(HEAD_FORMAT, "RPL".encode(), rest_pkt_size)
    sock.sendall(buf+confirm)
    return True

def get_reply_info(sock, user_no=NO_SPECIFIC):
    info = None
    reply = None
    message = None
    try:
        ready = select.select([sock], [], [], 35)
        #time.sleep(0.15)
        if ready[0]:
            buf = sock.recv(HEAD_SIZE)
            print("---**********i****"+str(len(buf)))
            rpl, rest_pkt_size = struct.unpack(HEAD_FORMAT, buf)
            info = sock.recv(rest_pkt_size)
    except Exception as error:
        print('error:',reply,message,':::::error:',error)
        return 'END', message
    else:
        message = info.decode(errors='ignore')
        reply = rpl.decode()
        xtrace("%s [%s] %s %s" % (SOCKET_IN, user_no, reply, message))
        return reply, message

def kill_myself():
    from sys import platform
    from os import system, getpid

    kill_str = {
        'linux': "kill -9 {PID}",
        'win32': "taskkill /f /pid {PID}"
    }
    shut_myself = kill_str[platform].format(getpid())
    system(shut_myself)


def check_name(user_no):
    ret = check_user_name(user_no)
    if ret[0][0] > 0:
        return True
    else:
        return False

def check_passwd(user_no, user_pass):
    ret = check_user_passwd(user_no, user_pass)
    if ret[0][0] > 0:
        return True
    else:
        return False