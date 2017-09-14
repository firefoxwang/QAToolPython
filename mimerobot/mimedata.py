# coding:utf-8
'''  这个py文件是用来配置微信返回的参数的'''

from deletealiuat2_1 import *


def mobile_sms(phoneNo):
    conn = pymysql.connect(host='yourhost', user='lingbo.wang', passwd='yoursecret', db='db',
                           charset='utf8')

    cur = conn.cursor()
    # cur.execute(
    #    "SELECT  content,createtime from SMS_HISTORY where phoneNo ={0} ORDER BY createTime DESC ".format(int(mobile)))
    cur.execute("SELECT content,createtime from SMS_HISTORY where phoneNo ='" + phoneNo + "' ORDER BY createTime DESC")

    sms = cur.fetchone()  # 抓取最新一条信息
    content = sms[0]
    createtime = sms[1]
    print content, createtime
    message = content + str(createtime)  # 从 mysql中取出来的是datetime.datetime格式
    cur.close()
    conn.close()

    return message


def data_handle(mobile, handle):
    if handle == u'11':  # 删除所有数据
        redis_delete = 1  # 确认删除redis
        baseinfo = 1  # 确认删除数据库数据
        mobile, memberid, loan_id, dataflage = memberinfo(mobile)
        if dataflage == 0:
            openid = wechatinfo(memberid=memberid)
            delete_redis_key(memberid=memberid, openid=openid, loan_id=loan_id, mobile=mobile,
                             redis_delete=redis_delete)
            del_sql_serverinfo(memberid=memberid, loan_id=loan_id, mobile=mobile, baseinfo=baseinfo)
            data_handle_box = u'All delete ok'
        elif dataflage == 1:
            print "oshit,you have done"
            data_handle_box = u'你的信息已经删除了，不要重复尝试'
        else:
            data_handle_box = u'请私聊我，有意外情况发生了'
    elif handle == u'10':
        redis_delete = 1  # 删除redis
        baseinfo = 0  # 只删除钱包数据
        mobile, memberid, loan_id, dataflage = memberinfo(mobile)
        if dataflage == 0:
            openid = wechatinfo(memberid=memberid)
            delete_redis_key(memberid=memberid, openid=openid, loan_id=loan_id, mobile=mobile,
                             redis_delete=redis_delete)
            del_sql_serverinfo(memberid=memberid, loan_id=loan_id, mobile=mobile, baseinfo=baseinfo)
            data_handle_box = u' delete redis and wallet ok'
        elif dataflage == 1:
            print "oshit,you have done"
            data_handle_box = u'你的信息已经删除了，不要重复尝试'
        else:
            data_handle_box = u'请私聊我，有意外情况发生了'
    elif handle == u'00':
        redis_delete = 0  # 不删除redis
        baseinfo = 0  # 值删除钱包数据
        mobile, memberid, loan_id, dataflage = memberinfo(mobile)
        if dataflage == 0:
            openid = wechatinfo(memberid=memberid)
            delete_redis_key(memberid=memberid, openid=openid, loan_id=loan_id, mobile=mobile,
                             redis_delete=redis_delete)
            del_sql_serverinfo(memberid=memberid, loan_id=loan_id, mobile=mobile, baseinfo=baseinfo)
            data_handle_box = u'delete wallet ok'
        elif dataflage == 1:
            print "oshit,you have done"
            data_handle_box = u'你的信息已经删除了，不要重复尝试'
        else:
            data_handle_box = u'请私聊我，有意外情况发生了'
    else:
        data_handle_box = u'please checkout and reinput your number '

    return data_handle_box  # 用这个发送信息给微信
