
#-*-coding:utf-8-*-

from DBMethods import DBMethods

def check_user_name(user_name):
    db_str = "select count(*) from serviceApp_userinf where user_name='%s';"
    db_str %= (user_name)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(db_str)
    return ret

def check_user_passwd(user_name, user_passwd):
    db_str = "select count(*) from serviceApp_userinf where binary user_name='%s' and binary user_passwd=password('%s');"
    db_str %= (user_name, user_passwd)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(db_str)
    return ret

# 用户增珊改查
def add_user_info(user_name, user_nickname="小修", user_sex="男", user_mask="Its a lazy man!", user_passwd="123456"):
    values= (user_name, user_nickname, user_sex, user_mask, user_passwd)
    db_str = "insert into serviceApp_userinf (user_name,user_nickname, user_grant, user_sex, user_mask, user_passwd) values ('{0}', '{1}', 0, '{2}', '{3}', password('{4}'));"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret 

def get_user_info():
    db_str = "select * from serviceApp_userinf where user_grant=0;"
    db_conn = DBMethods()
    ret = db_conn.selectMethods(db_str)
    return ret

def update_user_info(user_id, user_name, user_nickname, user_sex, user_mask):
    values= (user_id, user_name, user_nickname, user_sex, user_mask)
    db_str = "update serviceApp_userinf set user_name='{1}', user_nickname='{2}',user_sex='{3}',user_mask='{4}' where user_id = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret   

def update_user_password(user_no, old_passwd, new_passwd):
    values= (user_no, old_passwd, new_passwd)
    db_str = "update serviceApp_userinf set user_passwd=password('{2}') where user_name = '{0}' and user_passwd=password('{1}');"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

def del_user_info(user_id):
    values= (user_id)
    db_str = "delete from serviceApp_userinf where user_id = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

def reset_user_password(user_id):
    values= (user_id)
    db_str = "update serviceApp_userinf set user_passwd='123456' where user_id = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

# 汽修零件增删改差
def add_car_part( partName, partNumber, partPrice, partDate):
    values= (partName, partNumber, partPrice, partDate)
    db_str = "insert into serviceApp_carparts (partName, partNumber, partPrice, partDate) values ('{0}', {1}, {2}, '{3}');"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret 

def get_car_parts():
    dbStr = "select * from serviceApp_carparts;"
    #dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def del_car_part(partId):
    values= (partId)
    db_str = "delete from serviceApp_carparts where partId = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret



# 汽修工人功能

# repairPrice 通过carparts表查询 
 
def add_repair_info(user_id,repair_carName, repair_carPhone, partDetails, repair_fault, repairDetails, repairMask,repairingDate):
    try:
        partId, partNum = partDetails.split('*')
        partPrice=get_repairPrice(int(partId))
        totalPrice = partPrice * int(partNum)
    except Exception:
        totalPrice = 0.0
    values= (user_id,repair_carName, repair_carPhone, partDetails, repair_fault, repairDetails, repairMask,totalPrice,repairingDate)
    db_str = "insert into serviceApp_repairinfo (personId_id, repair_carName, repair_carPhone, partDetails,repair_fault, repairDetails, repairMask, totalPrice, repairingDate) values ({0}, '{1}', '{2}', '{3}', '{4}','{5}','{6}',{7},'{8}');"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

def change_repair_status(repairId, repairdDate):
    values=(repairId, repairdDate)
    db_str = "update serviceApp_repairinfo set repair_status=1, repairdDate='{1}' where repairId={0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret


def get_repairPrice(partId):
    values = (partId)
    db_str = "select partPrice from serviceApp_carparts where partId={0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def get_user_id(user_no):
    values = (user_no,)
    print(user_no)
    db_str = "select user_id from serviceApp_userinf where user_name='{0}';"
    dbStr = db_str.format(*values)
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret 

def get_user_name(user_id):
    values = (user_id)
    print(user_id)
    db_str = "select user_name from serviceApp_userinf where user_id={0};"
    dbStr = db_str.format(values)
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)

def get_repairing(user_id=None):
    values = (user_id)
    if user_id is None:
        db_str = "select * from serviceApp_repairinfo where repair_status=0;"
    else:
        db_str = "select * from serviceApp_repairinfo where personId_id={0} and repair_status=0;"
        dbStr = db_str.format( values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def get_repair_info(user_id=None):
    values = (user_id)
    if user_id is None:
        db_str = "select * from serviceApp_repairinfo where repair_status=1;"
    else:
        db_str = "select * from serviceApp_repairinfo where personId_id={0} and repair_status=1;"
        dbStr = db_str.format( values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def get_admin_repair_info():
    dbStr = "select * from serviceApp_repairinfo ;"
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret


def del_repair_info(repairId):
    values= (repairId)
    db_str = "delete from serviceApp_repairinfo where repairId = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

