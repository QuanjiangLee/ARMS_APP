def get_now_time():
    TIMEFORMAT='%Y-%m-%d %H:%M:%S'
    currentTime =  time.strftime(TIMEFORMAT, time.localtime())
    return currentTime


def end_connection(self):
        try:
            remove_from_alive(self.user_no)
            close_conn(self.user_no)
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception as error:
            pass
        finally:
            self.sock.close()