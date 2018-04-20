#! /usr/bin/python3
#-*-coding:utf-8-*-

import socket
import time
import threading
import select
from threading import Thread
from mylog import log, xtrace, error_log, get_curtime
from common import send_info,reply_client, get_reply_info, check_name, check_passwd, kill_myself
HOST = "0.0.0.0"
PORT = 50005
TreadNum = 0
BIND_INFO = (HOST, PORT)

class MyThread(Thread):
    def __init__(self, sock_fd, clnt):
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
                if len(text.split('\n')) == 4:
                    user_no, user_pas, user_mac, user_ip = text.split('\n')
                    self.user_no = user_no
                    self.hostIP = user_ip
                else:
                    user_no, user_pas, user_mac = text.split('\n')
                    self.user_no = user_no
        except Exception as error:
            error_log("AUTH FAILED")
            print(error)
            reply_client(self.sock, "WRONG ARISE")
            return False

        # 检查该用户是否有效
        if not check_name(user_no):
            reply_client(self.sock, "INVALID CLIENT")
            error_log("INVALID CLIENT")
            return False

        # 检查用户名密码是否正确
        if not check_passwd(user_no, user_pas):
            reply_client(self.sock, "WRONG PASSWD")
            return False
       
        # 用户身份不合法
        reply_client(self.sock, "INVALID")
        return False

    def run(self):
        #time.sleep(1)
        # 验证用户身份
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
                error_log("AFTER REMOVE CLIENT")
                print(error)
                break
            '''
            if "DNF" == cmd:    # 获取特殊关键字
                # info 为客户端请求下载的文件类型
                if not send_file(sock, info, user_no):
                    self.disconnected = True
                    break
            elif "END" == cmd:
                # record user log off
                log("%s %s OFFLINE" % (user_no, self.hostIP))
                self.end_connection()
                break
            # 记录异常
            elif "LOG" == cmd:
                self.local_time = get_curtime()
                record_warnings(info, user_no, self.local_time)
                log(info, user_no, self.local_time)

            # 接受用户文件
            elif "UPD" == cmd:
                self.local_time = get_curtime()
                recv_file(self.sock, user_no, info, self.local_time)

            # 接收用户一次扫描上传文件
            elif "UPF" == cmd:
                self.local_time = get_curtime()
                recv_file(self.sock, user_no, info, self.local_time, 1)

                # 接收用户一次扫描上传文件
            elif "UPS" == cmd:
                self.local_time = get_curtime()
                recv_file(self.sock, user_no, info, self.local_time, 2)

            # 客户端发送"心跳"数据包,保持 TCP 连接
            elif "HBT" == cmd:
                reply_client(self.sock, "HBT", user_no)
            #    if is_client_on_task(user_no):
            #        print("%s on remote task" %user_no)

            # 通过用户工号获取对应的软件截止日期
            elif "TIM" == cmd:
                if "CTM" == info:
                    reply_client(self.sock, get_curtime(), user_no)
                elif "EPT" == info:
                    reply_client(self.sock, get_expired_time(), user_no)
            '''
        log("CLIENT OFFLINE %s %s " % (user_no, self.hostIP))
        try:
            self.end_connection()
        except Exception:
            pass

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
