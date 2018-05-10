#! /usr/bin/python3
#-*-coding:utf-8-*-
import select
import hashlib
import struct
import time
from mylog import xtrace, SOCKET_IN, SOCKET_OUT
from db_operate import check_user_name, check_user_passwd, add_user_info, get_user_info, update_user_info,del_user_info,\
reset_user_password, add_car_part, get_car_parts, update_car_part, del_car_part, get_repair_statistics, add_repair_info,\
get_repair_info, update_repair_info,del_repair_info
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
    ret = []
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["user_id"] = index[0]
            dict["user_name"] = index[1]
            dict["user_nickname"] = index[2]
            dict["user_grant"] = index[3]
            dict["user_sex"] = index[4]
            dict["user_mask"] = index[5]
            ret.append(dict)
    return ret

def com_get_car_parts():
    ret_count = get_car_parts()
    ret = []
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["partId"] = index[0]
            dict["personId"] = index[1]
            dict["partName"] = index[2]
            dict["partNumber"] = index[3]
            dict["partType"] = index[4]
            dict["partSize"] = index[5]
            dict["partPrice"] = index[6]
            dict["partDate"] = index[6]
            ret.append(dict)
    return ret

def com_get_repair_statistics():
    ret_count = get_repair_statistics(sta_type='normal',curDay='today')
    ret = []
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["repairId"] = index[0]
            dict["repairName"] = index[1]
            dict["totalPrice"] = index[2]
            dict["repairDetails"] = index[3]
            dict["partDetails"] = index[4]
            dict["repairDate"] = index[5]
            dict["personId"] = index[6]
            ret.append(dict)
    return ret

def com_get_repair_info(user_id=None):
    ret_count = get_repair_info(user_id)
    ret = []
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["repairId"] = index[0]
            dict["repairName"] = index[1]
            dict["totalPrice"] = index[2]
            dict["repairDetails"] = index[3]
            dict["partDetails"] = index[4]
            dict["repairDate"] = index[5]
            dict["personId"] = index[6]
            ret.append(dict)
    return ret

def com_add_user_info(info):
    user_name, user_nickname, user_sex, user_mask, user_passwd = info.split('\n')
    set_result = add_user_info(user_name, user_nickname, user_sex, user_mask, user_passwd)
    if set_result > 0:
        return True
    else:
        return False
   
def com_update_user_info(info):
    user_id, user_name, user_nickname, user_sex, user_mask = info.split('\n')
    set_result = update_user_info(user_id, user_name, user_nickname, user_sex, user_mask)
    if set_result > 0:
        return True
    else:
        return False

def com_del_user_info(info):
    user_id = info.split('\n')
    set_result = del_user_info(user_id)
    if set_result > 0:
        return True
    else:
        return False

def com_reset_user_password(info):
    user_id = info.split('\n')
    set_result = reset_user_password(user_id)
    if set_result > 0:
        return True
    else:
        return False

def com_add_car_part(info):
    user_id, partName, partNumber, partType, partSize, partPrice = info.split('\n')
    set_result = add_car_part(user_id, partName, partNumber, partType, partSize, partPrice)
    if set_result > 0:
        return True
    else:
        return False

def com_update_car_part(info):
    partId,partName, partNumber, partType, partSize, partPrice = info.split('\n')
    set_result = update_car_part(partId,partName, partNumber, partType=None, partSize=0, partPrice=0.0)
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
def com_add_repair_info(info):
    user_id, repairName, partDetailsDict, repairDetails = info.split('\n')
    set_result = add_repair_info(user_id, repairName, partDetailsDict, repairDetails)
    if set_result > 0:
        return True
    else:
        return False

def com_update_repair_info(info):
    repairId, repairName,partDetailsDict, repairDetails = info.split('\n')
    set_result = update_repair_info(repairId, repairName,partDetailsDict, repairDetails)
    if set_result > 0:
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
