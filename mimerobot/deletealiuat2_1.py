# coding:utf-8
''' 新增的删除语句，可以写在这个py文件里 ,可以独立运行 脚本'''
import pymysql
import pyodbc
import logging
import redis

redis_config = {"host": "host",
                "port": "6379",
                "password": "passwd"
                }
sqlserver_config = {"DRIVER": "{SQL Server}",
                    "SERVER": "192.168.10.7",
                    "DATABASE": "memedaidb",
                    "UID": "lingbo.wang",
                    "PWD": "passwd",
                    "charset": "utf-8",
                    }
mysql_config = {"host": "192.168.10.2",
                "user": "lingbo.wang",
                "passwd": "passwd",
                "charset": "utf8",
                }
redis_sit_config = {"host": "99.48.66.13",
                    "port": "6379",
                    "password": "passwd"
                    }
sqlserver_sit_config = {"DRIVER": "{SQL Server}",
                        "SERVER": "99.48.66.112",
                        "DATABASE": "memedaidb",
                        "UID": "lingbo.wang",
                        "PWD": "passwd",
                        "charset": "utf-8",
                        }
mysql_sit_config = {"host": "192.168.10.2",
                    "user": "ingbo.wang",
                    "passwd": "passwd",
                    "charset": "utf8",
                    }


def sql_info(memberid, loan_id, mobile):
    # 删除用户数据
    delete_user_sql = "sql"
    # 删除账务数据
    delete_loan_sql = '''sql'
                    '''.format(str(loan_id), memberid)
    # 删除钱包数据
    delete_wallet_sql = '''sql'''.format(str(mobile), memberid)

    # 删除sdk数据
    delete_wallet_sdk = '''sql'''.format(mobile)

    return delete_loan_sql, delete_user_sql, delete_wallet_sdk, delete_wallet_sql


def redis_connect(dbase=1):
    db = dbase
    pool = redis.ConnectionPool(host=redis_config["host"], password=redis_config["password"], port=6379, db=db)
    r = redis.Redis(connection_pool=pool)
    return r


def mysql_connect():
    conn_mysql = pymysql.connect(host=mysql_config["host"], user=mysql_config["user"], passwd=mysql_config["passwd"],
                                 charset="utf8")
    cur_mysql = conn_mysql.cursor()
    return cur_mysql, conn_mysql


def sql_server_connect():
    conn_sqlserver = pyodbc.connect(DRIVER=sqlserver_config["DRIVER"], server=sqlserver_config["SERVER"],
                                    database=sqlserver_config["DATABASE"], uid=sqlserver_config["UID"],
                                    pwd=sqlserver_config["PWD"], charset="utf-8")
    cur_sql = conn_sqlserver.cursor()
    return cur_sql, conn_sqlserver


def delete_redis_key(memberid, openid, loan_id, mobile, redis_delete):  # 删除redis数据
    if redis_delete == 1:  # 确认是否需要删除redis
        member_key = "*" + memberid + "*"
        openid_key = "*" + openid + "*"
        loan_id_key = "*" + loan_id + "*"
        mobile_key = "*" + mobile + "*"

        dblist = [1, 3, 4]  # 需要加db的
        for db in dblist:
            redis_delet_connect = redis_connect(dbase=db)  # 导入的redis模块有.key获取Key，支持模糊搜索  .get  是得到value的值
            key_member = redis_delet_connect.keys(member_key)  # 返回的是list 不存在则为空字典
            key_openid = redis_delet_connect.keys(openid_key)
            key_loan_id = redis_delet_connect.keys(loan_id_key)
            key_mobile = redis_delet_connect.keys(mobile_key)
            keylist = [key_member, key_openid, key_loan_id, key_mobile]  # 所有的key的集合
            keydict = {"key_member": keylist[0], "key_openid": keylist[1], "key_loan_id": keylist[2],
                       "key_mobile": keylist[3]}  # 设置一个字典来容纳所有可能的的key
            truekeylist = []  # 每个db中真实存在的key值列表
            for i in keydict:
                keylength = len(keydict[i])
                if keylength > 0:  # 获取到的key不为空
                    for keylen in range(0, keylength):
                        truekeylist.append(keydict[i][keylen])  # 一个list中的所有的值都放入truekeylist 这个list中
                else:
                    print "数据库{0}中没有类似{1}的key".format(db, i)
            for truekey in truekeylist:
                if redis_delet_connect.delete(truekey):
                    print "删除数据库{0}中的key{1}成功".format(db, truekey)
                else:
                    print "删除失败，请重试"

        print "redis数据删除成功或redis中已无相关数据"
    elif redis_delete == 0:  # 确认不删除redis
        print "不删除redis"
    else:
        print "请重新运行并输入0或1"


def del_sql_serverinfo(memberid, loan_id, mobile, baseinfo):  # 删除mysql跟sqlserver
    if baseinfo == 1:
        print "*********delete sql,mysql info **********"
        sqlser_cur, sqlserver_conn = sql_server_connect()
        mysql_cur, mysql_conn = mysql_connect()
        delete_loan_sql, delete_user_sql, delete_wallet_sdk, delete_wallet_sql = sql_info(memberid=memberid,
                                                                                          loan_id=loan_id,
                                                                                          mobile=mobile)
        sqlser_cur.execute(delete_user_sql)  # 执行删除sqserver用户信息
        sqlser_cur.execute(delete_loan_sql)  # 执行删除账务信息
        mysql_cur.execute(delete_wallet_sql)  # 执行删除钱包数据
        mysql_cur.execute(delete_wallet_sdk)  # 执行删除sdk数据
        sqlserver_conn.commit()  # 关闭连接
        sqlser_cur.close()
        sqlserver_conn.close()
        mysql_conn.commit()
        mysql_cur.close()
        mysql_conn.close()
        print "**********Done*********"
    elif baseinfo == 0:
        print "************delete mysql info**********"
        mysql_cur, mysql_conn = mysql_connect()
        delete_loan_sql, delete_user_sql, delete_wallet_sdk, delete_wallet_sql = sql_info(memberid=memberid,
                                                                                          loan_id=loan_id,
                                                                                          mobile=mobile)
        mysql_cur.execute(delete_wallet_sql)  # 执行删除钱包数据
        mysql_cur.execute(delete_wallet_sdk)  # 执行删除sdk数据
        mysql_conn.commit()
        mysql_cur.close()
        mysql_conn.close()
        print "**********Done*********"
    else:
        print "请重新运行，并输入0或1"


def memberinfo(mobile):
    have_no_data = 0 #默认是有数据的
    mysql_cur, mysql_conn = mysql_connect()
    result_apply_info = mysql_cur.execute(
        "sql WHERE cellphone = {0}".format(int(mobile)))  # 查找memberid
    if result_apply_info == 1:
        memberid = str(mysql_cur.fetchone()[0])  # fetchone的值为tuple
        result_monkey_box_order = mysql_cur.execute(
            "sql ={0}".format(int(memberid)))  # 查看是否有订单值
    elif result_apply_info == 0:
        print "mysql中无相关数据"
        #os._exit(0)
        memberid,loan_id,have_no_data = '123445','1234565',1   # have_no_data为1表示没有mysql数据
        return mobile, memberid, loan_id, have_no_data
    else:
        pass
    if result_apply_info == 1 and result_monkey_box_order == 0:  # 钱包申请表优质但是订单表没数据
        loan_id = "12345678"  # 订单号
        print "手机号{0}无订单信息".format(mobile)
        mysql_cur.close()  # 关闭cur
        mysql_conn.close()  # 关闭连接
        return mobile, memberid, loan_id, have_no_data

    elif result_apply_info and result_monkey_box_order:  # 有订单
        mysql_cur.execute(
            "sql = {0}".format(memberid))  # 申请表有值且订单表有数据
        # 先只查一个订单
        loan_id = mysql_cur.fetchone()[0]
        mysql_cur.close()  # 关闭cur
        mysql_conn.close()  # 关闭连接
        return mobile, memberid, loan_id, have_no_data


def wechatinfo(memberid):
    sqlser_cur, sqlserver_conn = sql_server_connect()
    sqlser_cur.execute("select top 10 OPENID from crm.MEMBER_WECHAT where MEMBER_ID = {0}".format(memberid))
    result = sqlser_cur.fetchone()  # sql执行后不会返回0或1，只能用结果来判断
    if isinstance(result, pyodbc.Row):  # fetch 取出的是tuple类型的值
        openid = result[0]    # 取出str
        return openid
    else:
        print "不是微信用户"
        openid = "12345678"  # 删除openid为12345678的值
        return openid
    sqlser_cur.close()  # 关闭cur
    sqlserver_conn.close()  # 关闭连接


def main():
    try:
        mobile = raw_input("请输入手机号码\n")
        mobile, memberid, loan_id, dataflage = memberinfo(mobile)
        if dataflage == 0:
            openid = wechatinfo(memberid=memberid)
            redis_delete = int(raw_input("需要删除redis请按1,否则请按0\n"))
            delete_redis_key(memberid=memberid, openid=openid, loan_id=loan_id, mobile=mobile, redis_delete=redis_delete)
            print "删除redis数据成功或者不需要删除redis数据！！！"
            baseinfo = int(raw_input("需要删除所有数据请输入1 ，值删除钱包数据按0\n"))
            del_sql_serverinfo(memberid=memberid, loan_id=loan_id, mobile=mobile, baseinfo=baseinfo)
        elif dataflage == 1:
            print "oshit,you have done"
        else:
            pass
    except Exception as ex:
        logging.exception('caught an error')  # 异常捕获的时候调用这个方法，捕获的异常连同堆栈追踪信息都会被自动记录下来。
        print "delete redisinfo has failure！！！", ex


if __name__ == '__main__':
    main()
