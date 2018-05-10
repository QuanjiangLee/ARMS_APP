
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
def add_user_info(user_name, user_nickname="小修", user_sex="男", user_mask="It\'s a lazy man!", user_passwd="123456"):
    values= (user_name, user_nickname, user_sex, user_mask, user_passwd)
    db_str = "insert into serviceApp_userinf (user_name， user_nickname，user_grant, user_sex， user_mask， user_passwd) values ('{0}', '{1}', 0, '{2}', '{3}', password('{4}'));"
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
    db_str = "update serviceApp_userinf set user_name='{1}'， user_nickname='{2}'， user_sex='{3}'， user_mask='{4}' where user_id = {0};"
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
def add_car_part(user_id, partName, partNumber, partType=None, partSize=0, partPrice=0.0):
    values= (user_id, partName, partNumber, partType, partSize, partPrice)
    db_str = "insert into serviceApp_carparts (personId_id, partName, partNumber, partType, partSize, partPrice) values ({0}, '{1}', {2}, '{3}', '{4}', {5});"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret 

def get_car_parts():
    db_str = "select * from serviceApp_carparts;"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def update_car_part(partId,partName, partNumber, partType=None, partSize=0, partPrice=0.0):
    values= (partId,partName, partNumber, partType, partSize, partPrice)
    db_str = "update serviceApp_carparts set partName='{1}', partNumber={2}, partType='{3}', partSize='{4}', partPrice={5} where partId = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

def del_car_part(partId):
    values= (partId)
    db_str = "delete from serviceApp_carparts where partId = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

# 汽修情况统计查看
def get_repair_statistics(sta_type='normal',curDay='today'):
    '''sta_type = ['normal', 'day']
    '''
    values = (sta_type, curDay)
    if sta_type is 'normal':
        dbStr = "select * from serviceApp_repairinfo;"
    elif sta_type is 'day':
        if curDay is 'today':
            dbStr = "select * from serviceApp_repairinfo where date(repairDate) = curdate();"
        else:
            db_str = "select * from serviceApp_repairinfo where date(repairDate) = date_sub('{1}', interval 0 day);"
            dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret



# 汽修工人功能

# repairPrice 通过carparts表查询 

def add_repair_info(user_id, repairName, partDetailsDict, repairDetails='No details'):
    totalPrice = 0.0
    partDetails = ''
    for part in partDetailsDict:    
        totalPrice += get_repairPrice(part["partId"])[0][0] * part['partNumber']
        partDetails += part['partName'] +' ' + part['partNumber'] +'\n'
    values= (repairId, repairName, partDetails, totalPrice, repairDetails)
    db_str = "insert into serviceApp_repairinfo (personId_id, repairName,partDetails, totalPrice, repairDetails) values ({0}, '{1}', '{2}', {3}, '{4}');"
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

def get_repair_info(user_id=None):
    values = (user_id)
    if user_id is None:
        db_str = "select * from serviceApp_repairinfo;"
    else:
        db_str = "select * from serviceApp_repairinfo where personId_id={0};"
        dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.selectMethods(dbStr)
    return ret

def update_repair_info(repairId, repairName,partDetailsDict, repairDetails='No details'):
    totalPrice = 0.0
    partDetails = ''
    for part in partDetailsDict:    
        totalPrice += get_repairPrice(part["partId"])[0][0] * part['partNumber']
        partDetails += part['partName'] +' ' + part['partNumber'] +'\n'
    values= (repairId, repairName, partDetails, totalPrice, repairDetails)
    db_str = "update serviceApp_repairinfo set repairName='{1}',partDetails='{2}', totalPrice={3}, repairDetails='{4}' where repairId={0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

def del_repair_info(repairId):
    values= (repairId)
    db_str = "delete from serviceApp_repairinfo where repairId = {0};"
    dbStr = db_str.format( *values )
    print(dbStr)
    db_conn = DBMethods()
    ret = db_conn.updateMethods(dbStr)
    return ret

