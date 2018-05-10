from enum import Enum

from mylog import log, xtrace, error_log, get_curtime
from common import send_info,reply_client, get_reply_info, check_name, check_passwd, kill_myself

GLOBAL_REMOTE_CONTROL = {}

class kProccessState(Enum):
    kAuthing = 1
    kNeedRegister = 2
    kAuthSuccess = 3

    kFirstScan = 10
    kSecondScan = 11
    kSelfScan = 12
    kMakeKwFail = 13
    kMakeKwSuccess = 14

    kHbt = 33

    # 任务处理失败的情况，需关闭客户端的连接
    kAuthFail = 100
    kEndConnecion = 101
    kMacDiff = 102
    kRecvFile = 10010
    kNeedFileHash = 10011
    kNeedFileInfo = 10012
    kRecvDone = 10013
    kRemoteCtl = 10020
    kUploadFile = 10021
    kCtlSuccess = 10022
    kCtlFail = 10023


kOK = "OK"
kFail = "FAILED"
kHbt = "HBT"


class kFileState(Enum):
    kOpenFail = 1001
    kExisted = 1002
    kFileNameIsNone = 1003


class Client:
    def __init__(self, addr):
        self.user_name = None
        self.__response = ""
        self.user_addr = None
        self.current_time = get_curtime()
        self.__is_login = False

    def is_login(self):
        return self.__is_login

    def auth(self, text):
        # 接收并解析用户发来的信息，进行身份认证
        self.process_state = kProccessState.kAuthFail
        try:
            if text is None:
                return False
            else:
                user_name, user_passwd = text.split('\n')
        except Exception as error:
            error_log("AUTH FAILED")
            print(error)
            self.__response = "WRONG ARISE ABOUT SOCKET COMMUNICATION"
            return False
        self.user_name = user_name
        # 检查该用户是否有效(数据库中是否有该用户)
        if not check_name(user_name):
            self.__response = "NEED REGISTER"
            error_log("NEED REGISTER")
            return False

        # 检查用户名密码是否正确
        if not check_passwd(user_name, user_passwd):
            self.__response = "WRONG PASSWD"
            return False
        self.process_state = kProccessState.kAuthSuccess
        return True

'''
    def insert_user_info(self):
        insert_2alive_list(self.__user_no)
        set_user_login(self.__user_no, self.user_addr, 1)

    def insert_2alive_list(seq):
        with global_mutex:
            GLOBAL_REMOTE_CONTROL[seq] = {}
            GLOBAL_REMOTE_CONTROL[seq]['status'] = CommandStatus.NO_TASK
            GLOBAL_REMOTE_CONTROL[seq]['cmd'] = None
            GLOBAL_REMOTE_CONTROL[seq]['args'] = None
            GLOBAL_REMOTE_CONTROL[seq]['rst'] = None
        return True
'''
    def hbt(self):
        self.__response = kHbt
        self.process_state = kProccessState.kHbt

    def scan(self, data):
        pass

    def get_addr(self):
        return self.user_addr

    def get_response(self):
        return self.__response

    def client_offline(self):
        log("%s %s OFFLINE" % (self.__user_no, self.user_addr))
        remove_from_alive(self.get_user_no())
        close_conn(self.get_user_no())
        self.__is_login = False
        self.process_state = kProccessState.kEndConnecion

    def process_cmd(self, cmd, cmd_info):
        if "RPL" == cmd:
            if self.process_state == kProccessState.kNeedFileHash:
                self.check_upload_existed(cmd_info, self.recv_file_arg)
            elif self.process_state == kProccessState.kNeedFileInfo:
                self.send_upload_num(cmd_info, self.recv_file_arg)
        # 远程控制执行成功，更新状态位
        elif RemoteControl.CTL_RPL_OK == cmd or RemoteControl.CTL_RPL_FAILED == cmd:
            self.update_task_state(cmd, cmd_info)
        elif "ATH" == cmd:
            if self.process_state == kProccessState.kNeedRegister:
                # 注册成功
                self.register(cmd_info)
            else:
                self.auth(cmd_info)
        elif "DNF" == cmd:
            self.send_keywords_file(cmd_info)
        elif "END" == cmd:
            self.proccess_state = kProccessState.kEndConnecion
           # self.client_offline()
        # 记录异常
        elif "LOG" == cmd:
            curt_time = get_curtime()
            record_warnings(cmd_info, self.__user_no, curt_time)
            #log(cmd_info, self.__user_no, curt_time)
            self.__response = kOK
        # 接受用户报警文件
        elif "UPD" == cmd:
            self.recv_file_arg = None
            self.current_time = get_curtime()
            self.recv_file(cmd_info)
            # self.__user_socket.end_connection(self.__user_no)
            # 接收用户全盘扫描需要上传的文件
        elif "UPF" == cmd:
            self.recv_file_arg = FIRST_UPLOAD
            self.current_time = get_curtime()
            self.recv_file(cmd_info)

        # 接收用户快速扫描需要上传文件
        elif "UPS" == cmd:
            self.recv_file_arg = SECOND_UPLOAD
            self.current_time = get_curtime()
            self.recv_file(cmd_info)
        elif "INF" == cmd:
            if self.__ctl_status == RemoteControl.CTL_UPLOAD_FIRST:
                self.__response = get_first_upload_file_info(self.__ctl_args)
            elif self.__ctl_status == RemoteControl.CTL_UPLOAD_SECOND:

                self.__response = get_second_upload_file_info(self.__ctl_args)
            self.process_state = kProccessState.kUploadFile
        # 询问服务器时间和服务器过期时间
        elif "TIM" == cmd:
            if "CTM" == cmd_info:
                self.__response = get_curtime()
            elif "EPT" == cmd_info:
                self.__response = get_expired_time()
        # 与客户端保持心跳
        elif "HBT" == cmd:
            self.hbt()
        return self.process_state

