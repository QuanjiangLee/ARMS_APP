
#-*-coding:utf-8-*-

from DBMethods import DBMethods

def check_user_name(userNo):
    db_str = "select count(*) from userInf where userNo='%s';"
    db_str %= (userNo)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(db_str)
    return ret

def check_user_passwd(userNo, userPasswd):
    db_str = "select count(*) from userInf where binary userNo='%s' and binary userPasswd=password('%s');"
    db_str %= (userNo, userPasswd)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(db_str)
    return ret  