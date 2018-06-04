#! /usr/bin/python3
#-*-coding:utf-8-*-
import select
import hashlib
import struct
import time
from mylog import xtrace, SOCKET_IN, SOCKET_OUT, get_curtime
from db_operate import *
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


def com_check_name(user_no):
    ret = check_user_name(user_no)
    if ret[0][0] > 0:
        return True
    else:
        return False

def com_check_passwd(user_no, user_pass):
    ret = check_user_passwd(user_no, user_pass)
    if ret[0][0] > 0:
        return True
    else:
        return False

def com_get_user_info():
    ret_count = get_user_info()
    ret = ''

    if len(ret_count) > 0:
        for index in ret_count:
            ret += str(index[0])+'|'+str(index[1])+'|'+str(index[2])+'|'+str(index[4])+'|'+str(index[5])+'\n'
    return ret


def com_get_car_parts():
    ret_count = get_car_parts()
    ret = ''

    if len(ret_count) > 0:
        for index in ret_count:
            ret += str(index[0])+'|'+str(index[1])+'|'+str(index[2])+'|'\
                +'hah'+'|'+'100m'+'|'+str(index[5])+'|'\
                +str(index[6])+'|'+str(index[7])+'\n'
    return ret



def com_get_repairing(user_no=None):
    if user_no:
        user_id = get_user_id(user_no)[0][0]
        ret_count = get_repairing(user_id)
    else:
        ret_count = get_repairing()
    ret = ''
    if len(ret_count) > 0:
        for index in ret_count:
            ret += str(index[0])+'|'+str(index[1])+'|'+str(index[3])+'|'\
                +str(index[8])+'|'+str(index[6])+'|'+str(index[9])+'|'\
                +str(index[10])+'\n'
    return ret

def com_get_repair_info(user_no=None):
    if user_no:
        user_id = get_user_id(user_no)[0][0]
        ret_count = get_repair_info(user_id)
    else:
        ret_count = get_repairing()
    ret = ''
    if len(ret_count) > 0:
        for index in ret_count:
            ret += str(index[0])+'|'+str(index[1])+'|'+str(index[3])+'|'\
                +str(index[8])+'|'+str(index[6])+'|'+str(index[9])+'|'\
                +str(index[10])+'|'+str(index[11])+'\n'
    return ret


def com_admin_repair_info():
    ret_count = get_admin_repair_info()
    ret = ''
    if len(ret_count) > 0:
        for index in ret_count:
            ret += str(index[0])+'|'+str(index[1])+'|'+str(index[3])+'|'\
                +str(index[8])+'|'+str(index[6])+'|'+str(index[9])+'|'\
                +str(index[10])
            if str(index[11]):
                ret += '|'+str(index[11])+'\n'
            else:
                ret += '|'+'正在维修'+'\n'
    return ret

def com_add_user_info(info):
    user_name, user_nickname, user_sex = info.split('\n')
    set_result = add_user_info(user_name, user_nickname, user_sex)
    if set_result > 0:
        return True
    else:
        return False
   
def com_update_user_info(info):
    user_id, user_name, user_nickname, user_sex = info.split('\n')
    set_result = update_user_info(user_id, user_name, user_nickname, user_sex)
    if set_result > 0:
        return True
    else:
        return False

def com_update_user_password(info,user_no):
    new_passwd = info.split("\n")[0]
    set_result = update_user_password(user_no, new_passwd)
    if set_result > 0:
        return True
    else:
        return False

def com_del_user_info(info):
    user_id = info.split("\n")[0]
    set_result = del_user_info(user_id)
    if set_result > 0:
        return True
    else:
        return False

def com_reset_user_password(info):
    user_id = info.split("\n")[0]
    set_result = reset_user_password(user_id)
    if set_result > 0:
        return True
    else:
        return False

def com_add_car_part(info):
    partName, partNumber, partPrice = info.split('\n')
    set_result = add_car_part(1, partName, partNumber, None, 0, partPrice)
    if set_result > 0:
        return True
    else:
        return False


def com_del_car_part(info):
    partId = info.split('\n')
    set_result = del_car_part(partId)
    if set_result > 0:
        return True
    else:
        return False

def com_add_repair_info(info, user_no):
    repair_carName, repair_carPhone, partDetails, repair_fault, repairDetails, repairMask = info.split('\n')
    repairingDate = get_curtime()
    user_id  = get_user_id(user_no)[0][0]
    set_result = add_repair_info(user_id,repair_carName, repair_carPhone, partDetails, repair_fault, repairDetails, repairMask,repairingDate)
    if set_result > 0:
        return True
    else:
        return False

def com_change_repair_status(info):
    repairId = info.split('\n')[0]
    repairdDate = get_curtime()
    ret = change_repair_status(repairId, repairdDate)
    if ret > 0:
        return True
    else:
        return False


def com_del_repair_info(info):
    repairId = info.split('\n')
    set_result = del_repair_info(repairId)
    if set_result > 0:
        return True
    else:
        return False
