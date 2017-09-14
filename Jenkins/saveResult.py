#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
保存新框架的入库结果
"""
import pymysql
import jenkins
import sys
import decimal
from xml.etree import ElementTree as ET

mysql_config = {"host": "99.48.66.40",
                "user": "wanglingbo",
                "passwd": "Wanglingbo@123",
                "charset": "utf8",
                }
# jenkins相关
jenkins_config = {"jenkins_url": "http://jenkins.immd.cn/", "username": "lingbo.wang", "password": "3ae0bef4aaea0d4dd43ff6f53443364b"}
auto2jenkins = {"UserTest": "user","UserDubbo":"userCore" ,"wechat":"walletWechat",
                "sdk-web": "sdk-web","sdk-gateway":"sdk-gateway", "wallet": "wallet-web",
                "repayment":"repayment","ups":"ups",
                "capital-conf-facade":"capital-config-facade","capital-mgmt-facade":"capital-mgmt-facade","cashloan":"cash-loan-web",
                "hermesAppSdk":"hermesApp_sdk","creditAudit":"credit-audit-core","creditTradeAudit":"credit-trade-audit-core",
                "Flow":"all"}  # 建立自动化项目跟jenkins项目的对应关系

jenkins2xml = {"user": "testng-user.xml", "walletSdk": "testng-sdk.xml"}

environment = sys.argv[1]
file = "/home/user/testng_results/testng-results.xml"

def mysql_connect():
    conn_mysql = pymysql.connect(host=mysql_config["host"], user=mysql_config["user"], passwd=mysql_config["passwd"],
                                 charset="utf8")
    cur_mysql = conn_mysql.cursor()
    return cur_mysql, conn_mysql

def result_write_db(caseResult,environment):
        server = jenkins.Jenkins(jenkins_config["jenkins_url"], username=jenkins_config['username'],
                                 password=jenkins_config["password"])
        mysql_cur, mysql_conn = mysql_connect()
        # 处理数据
        for item in caseResult.keys():
            last_build_number = server.get_job_info(auto2jenkins[item])['lastCompletedBuild']['number'] #获取jenkins任务最新成功构建版本号
            test_count = caseResult[item]['passed']+caseResult[item]['failed']+caseResult[item]['skipped']#用例总数
            test_fail = caseResult[item]['failed']+caseResult[item]['skipped']#失败用例数
            test_apr = int(decimal.Decimal(caseResult[item]['passed'])/decimal.Decimal(test_count)*decimal.Decimal(100))#成功比例
            insert_result_sql = " insert into autotest_result.report_result (project_name,start_time,end_time,build_number,test_apr,jenkins_name,environment,test_count,test_pass,test_fail,is_testng) " \
                                "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(item, caseResult[item]['start_time'], caseResult[item]['end_time'],
                                                                                last_build_number,test_apr, auto2jenkins[item], environment,test_count,caseResult[item]['passed'],test_fail,1)
            result = mysql_cur.execute(insert_result_sql)
            if(result==1):
                print u"{0}的用例执行结果入库成功".format(item)
            mysql_conn.commit()
        mysql_cur.close()  # 关闭cur
        mysql_conn.close()  # 关闭连接

#解析xml文件获取执行结果
def parseResult(file):
    caseResult = {}
    #得到文档元素对象
    tree = ET.parse(file)
    root = tree.getroot()
    suite = root.find("suite")
    test = suite.findall("test")
    #每个系统用例的成功和失败个数
    for eachEle in test:
        testName = eachEle.get("name")
        skipped = 0
        failed = 0
        passed = 0
        start_time = eachEle.get("started-at")
        end_time = eachEle.get("finished-at")
        #获取每个系统下的所有测试类
        classes = eachEle.findall("class")
        for classNow in classes:
            #获取每个测试类下的所有用例
            methods = classNow.findall("test-method")
            for method in methods:
                #判断是不是配置方法如beforeClass等
                if(method.get("is-config") is None):
                    if("PASS" in method.get("status")):
                        passed += 1
                    elif("FAIL" in method.get("status")):
                        failed += 1
                    else:
                        skipped += 1

        caseResult[testName] = {'skipped':skipped,'failed':failed,'passed':passed,'start_time':start_time,'end_time':end_time}

    return caseResult

if __name__ == '__main__':
    caseResult = parseResult(file)
    result_write_db(caseResult,environment)








