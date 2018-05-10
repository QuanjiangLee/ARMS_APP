#! /usr/bin/python3
#-*-coding:utf-8-*-

import socket
import time
import threading
import select
from threading import Thread
from mylog import log, xtrace, error_log, get_curtime
from common import send_info, reply_client, get_reply_info, kill_myself,com_check_name, com_check_passwd,\
com_add_user_info,com_get_user_info, com_update_user_info, com_del_user_info, com_reset_user_password,\
com_add_car_part, com_get_car_parts,com_update_car_part, com_del_car_part, com_get_repair_statistics,\
com_add_repair_info,com_get_repair_info, com_update_repair_info, com_del_repair_info
HOST = "0.0.0.0"
PORT = 50005
TreadNum = 0
BIND_INFO = (HOST, PORT)

class MyThread(Thread):
    def __init__(self, sock_fd, clnt):
        super().__init__()
        self.local_time = get_curtime()
        self.sock = sock_fd
        self.hostIP = clnt
        self.disconnected = False
        self.user_no = None

    def auth(self):
        # 发送认证消息
        send_info(self.sock, "ATH", "WHO ARE YOU")
        # 接收用编号
        try:
            # 获取用户命令
            text = get_reply_info(self.sock)[1]
            print("---text----",text)
            if text is None:
                return False
            else:
                user_no, user_pas = text.split('\n')
        except Exception as error:
            error_log("AUTH FAILED")
            print(error)
            reply_client(self.sock, "WRONG ARISE")
            return False

        # 检查该用户是否有效
        if not com_check_name(user_no):
            reply_client(self.sock, "INVALID USERNAME")
            error_log("INVALID USERNAME")
            return False

        # 检查用户名密码是否正确
        if not com_check_passwd(user_no, user_pas):
            reply_client(self.sock, "WRONG PASSWD")
            return False
        return user_no

    def run(self):
        '''            
        登录：ATH
        管理员：
        人员管理：AUC(add)  DUC(del) MUC(alter) SUC(select) RUP(重置密码)
        配件管理：APT DPT MPT SPT
        维修统计：RMS
        维修工：
        配件查看：SPT
        维修发起：SRO SPT(零件种类和数量)
        维修历史：SRH
        '''
        user_no = self.auth()
        if user_no == False:
            self.end_connection()
            return False
        while not self.disconnected:
            # 获取用户命令
            try:
                cmd, info = get_reply_info(self.sock, user_no)
                print("info+++++++++++",info,"++++++++++++cmd",cmd)
            except Exception as error:
                self.disconnected = True
                error_log("RECV INFO ERROR!")
                print(error)
                break
            if "SPT" == cmd:
                send_data = com_get_car_parts()
                if send_data:
                    send_info(self.sock, "SPT", send_info, user_no)
                else:
                    send_info(self.sock, "SPT", "WRONG SPT", user_no)
            elif "SUC" == cmd:
                send_data = com_get_user_info()
                if send_data:
                    send_info(self.sock, "SUC",send_info, user_no)
                else:
                    send_info(self.sock, "SUC", "WRONG SUC", user_no)

            elif "SRH" == cmd:
                send_data = com_get_repair_info()
                if send_data:
                    send_info(self.sock,"SRC", send_info, user_no)
                else:
                    send_info(self.sock,"SRC", "WRONG SRH", user_no)
            elif "RMS" == cmd:
                send_data = com_get_repair_statistics()
                if send_data:
                    send_info(self.sock, "RMS", send_info, user_no)
                else:
                    send_info(self.sock, "RMS", "WRONG RMS", user_no)
            elif "AUC" == cmd:
                if not com_add_user_info(info):
                    send_info(self.sock, "AUC","WRONG AUC", user_no)
                else:
                    send_info(self.sock, "AUC","AUC OK", user_no)

            elif "DUC" == cmd:
                if not com_del_user_info(info):
                    send_info(self.sock, "DUC", "WRONG DUC", user_no)
                else:
                    send_info(self.sock, "DUC", "DUC OK", user_no)
            elif "MUC" == cmd:
                if not com_update_user_info(info):
                    send_info(self.sock, "MUC", "WRONG MUC", user_no)
                else:
                    send_info(self.sock, "MUC","MUC OK", user_no)
            elif "RUP" == cmd:
                if not com_reset_user_password(info):
                    send_info(self.sock, "RUP", "WRONG RUP", user_no)
                else:
                    send_info(self.sock, "RUP", "RUP OK", user_no)
            elif "APT" == cmd:
                if not com_add_car_part(info):
                    send_info(self.sock, "APT", "WRONG APT", user_no)
                else:
                    send_info(self.sock, "APT", "APT OK", user_no)
            elif "DPT" == cmd:
                if not com_del_car_part(info):
                    send_info(self.sock, "DPT", "WRONG DPT", user_no)
                else:
                    send_info(self.sock, "DPT", "DPT OK", user_no)
            elif "MPT" == cmd:
                if not com_update_car_part(info):
                    send_info(self.sock, "MPT", "WRONG MPT", user_no)
                else:
                    send_info(self.sock, "MPT", "MPT OK", user_no)
            
            elif "SRO" == cmd:
                if not com_add_repair_info(info):
                    send_info(self.sock, "SRO", "WRONG RMS", user_no)
                else:
                    send_info(self.sock, "SRO", "RMS OK", user_no)
            elif "END" == cmd:
                # record user log off
                log("%s %s OFFLINE" % (user_no, self.hostIP))
                self.end_connection()
                break
        log("CLIENT OFFLINE %s %s " % (user_no, self.hostIP))
        try:
            self.end_connection()
        except Exception as err:
            print("[error]",err)

    def end_connection(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception as error:
            pass
        finally:
            self.sock.close()


if __name__ == "__main__":
    log("SERVER UP")
    # 服务启动
    service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    service.bind(BIND_INFO)
    service.listen(5)
    host, port = BIND_INFO
    log("MasterThread listening: %s:%d" % (host, port))
    
    while True:
        try:
            recvSock, (clnt_ip, clnt_port) = service.accept()
        except Exception as error:
            log("close server!")
            log("RESET ALL USER TO OFFLINE")
            log("SERVER DOWN")
            kill_myself() 
        else:          
            log("CONNECT FROM %s:%d" %(clnt_ip, clnt_port))
            TreadNum = TreadNum + 1
            print('TreadNum:',TreadNum)
            task = MyThread(recvSock, clnt_ip)
            task.setDaemon(True)
            task.start()
