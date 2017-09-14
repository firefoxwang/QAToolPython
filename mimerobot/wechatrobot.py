# coding:utf-8

'''要使用微信机器人的时候，需要运行这个py文件，需要mimedata跟deletealiuat2.1都在一个路径下'''

import re
import itchat

from mimedata import  *

@itchat.msg_register('Text')   # 只注册图片 其他不回应，针对个人
def text_(msg):
    msgtext = msg['Text']    # msg['Text']为unicode
    print msgtext
    if len(msgtext) == 11:  # 是手机号码，判断是来询问手机号的  手机号码 11位
        message = mobile_sms(phoneNo=msgtext)  # 查询手机号,sms为返回的验证码
        #itchat.send(msgtext, message, msg['FromUserName'])
        itchat.send('%s: %s' % (msg['Type'], message), msg['FromUserName'])
    elif len(msgtext) == 13:  # 输入的是手机号码加上删除数据的比如 1515186376800
        mobile = msgtext[0:11]
        handle = msgtext[-2:]  # 倒数2个
        data_handle_box = data_handle(mobile=mobile, handle=handle)
        itchat.send('%s: %s' % (msg['Type'], data_handle_box), msg['FromUserName'])


@itchat.msg_register('Text', isGroupChat=True)
def text_reply(msg):
    if msg['IsAt']:
        msgtext = re.search(pattern=ur'[1-9]([0-9]{5,12})', string=msg['Content']).group()    # 用正则匹配到号码11位或者13位
        print msgtext
        if len(msgtext) == 11:  # 是手机号码，判断是来询问手机号的  手机号码 11位
            message = mobile_sms(phoneNo=msgtext)  # 查询手机号,sms为返回的验证码
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], message), msg['FromUserName'])
        elif len(msgtext) == 13:  # 输入的是手机号码加上删除数据的比如 1515186376800
            mobile = msgtext[0:11]
            handle = msgtext[-2:]  # 倒数2个
            data_handle_box = data_handle(mobile=mobile, handle=handle)
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], data_handle_box), msg['FromUserName'])
        else:
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], u'输入格式有误'), msg['FromUserName'])
itchat.auto_login(hotReload=True)
itchat.run()
