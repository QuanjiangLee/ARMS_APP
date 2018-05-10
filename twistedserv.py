import signal

from server import Server
from twisted.internet import reactor

def kill_myself(signum, frame):
    from os import system, getpid
    pid = getpid()
    shut_myself = "kill -9 " + str(pid)
    system(shut_myself)
    reactor.stop()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, kill_myself)
    signal.signal(signal.SIGTERM, kill_myself)
    # 加载配置文件
    server = Server()
    server.run()
