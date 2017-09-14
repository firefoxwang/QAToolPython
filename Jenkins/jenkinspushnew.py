#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
根据是否执行了该版本的自动化，判判断是否能发不到aliuat  需要给两个参数 jenkins项目名跟对应的构建号
"""
import logging
import os
import platform
from saveResult import *
from looptestng import *

jenkins_name = sys.argv[1]
jenkins_number = sys.argv[2]

# 执行路径
linuxpath = '/home/user/execution/Public/Soraka/robot_run.py '
#winpath = 'D:\\TEST\\AutoTestCase\\Public\\publiclibary\\robot_run.py '
#D:\TEST\AutoTestCase\Public\Soraka\robot_run.py
winpath = 'D:\\TEST\\AutoTestCase\\Public\\Soraka\\robot_run.py '


def oprerate_mysql(sql, mysql_config=mysql_config):
    conn_mysql = pymysql.connect(host=mysql_config["host"], user=mysql_config["user"], passwd=mysql_config["passwd"],
                                 charset="utf8")
    return_info = None

    try:
        if 'select' in sql.lower():
            conn_mysql.cursor().execute(sql)
            return_info = conn_mysql.cursor().fetchone()
        else:
            conn_mysql.cursor().execute(sql)
            conn_mysql.commit()
    except Exception, e:
        conn_mysql.rollback()
        logging.exception('caught an error')
        print e
    finally:
        conn_mysql.cursor().close()
        conn_mysql.close()
        return return_info


def gettestdb(jenkins_name, jenkins_number):
    mysql_cur, mysql_conn = mysql_connect()
    result = mysql_cur.execute(
        "SELECT * FROM `autotest_result`.`report_result` WHERE build_number = '{0}' AND jenkins_name = '{1}' AND environment = 'sit' ORDER BY start_time DESC".format(
            jenkins_number, jenkins_name))
    db = mysql_cur.execute(
        "SELECT  build_number FROM `autotest_result`.`report_result` WHERE jenkins_name = '{0}' AND environment = 'sit' ORDER BY start_time DESC".format(
            jenkins_name))
    db_number = str(mysql_cur.fetchone()[0])
    apr = mysql_cur.execute(
        "SELECT  test_apr,id FROM `autotest_result`.`report_result` WHERE jenkins_name = '{0}' AND environment = 'sit' ORDER BY start_time DESC".format(
            jenkins_name))
    dbresult = mysql_cur.fetchone()
    test_apr = str(dbresult[0])
    id = dbresult[1]
    project_name_log = mysql_cur.execute(
        "SELECT  project_name FROM `autotest_result`.`report_result` WHERE jenkins_name = '{0}' AND environment = 'sit' ORDER BY start_time DESC".format(
            jenkins_name))
    project_name = str(mysql_cur.fetchone()[0])
    testngsql = "SELECT  is_testng FROM `autotest_result`.`report_result` WHERE jenkins_name = '{0}' AND environment = 'sit' ORDER BY start_time DESC".format(
        jenkins_name)
    istestng_log = mysql_cur.execute(testngsql)
    istestng = mysql_cur.fetchone()[0] if istestng_log != 0 else None
    greensql ="SELECT Green_channel FROM `autotest_result`.`report_result` WHERE build_number = '{0}' AND jenkins_name = '{1}' AND environment = 'sit' ORDER BY start_time DESC".format(jenkins_number, jenkins_name)
    greenflag = mysql_cur.execute(greensql)
    greechannel = mysql_cur.fetchone()[0] if greenflag !=0 else None
    mysql_cur.close()  # 关闭cur
    mysql_conn.close()  # 关闭连接  Green_channel
    return result, db_number, test_apr, project_name, id, istestng, greechannel


def update_pushflag(jenkins_name, jenkins_number):
    # todo:对于新框架的用例结果，需要做轮训处理，以后再写

    """
    项目运行结束后，对最新的执行结果跟新flag，如果通过率为100则可以发布aliuat
    :param jenkins_name:
    :param jenkins_number:
    :return:
    """
    result, db_number, test_apr, project_name, id, istestng, greechannel = gettestdb(jenkins_name, jenkins_number)
    if int(test_apr) == 100:
        print "*******************************"
        print "*******************************"
        print "*******************************"
        print "自动化用例运行成功，项目发布到aliuat"
    else:
        print "*******************************"
        print "*******************************"
        print "*******************************"
        print "自动化用例运行失败，请查找原因后重新尝试发布到aliuat"
        os._exit(1)
    sql = "UPDATE `autotest_result`.`report_result` SET push2aliuat = '1' WHERE id = {0}".format(
        int(id))
    oprerate_mysql(sql)  # 跟新数据库的数据


def run_suite(istestng, project_name, jenkins_name):
    """
    选择运是运行新框架，还是旧框架的用例
    :param istestng:
    :param project_name:
    :param jenkins_name:
    :return:
    """
    realpath = getrealpath()
    if istestng is None:
        re_project_name = realpath + project_name + ' ' + 'jenkins'  # sit自动化路径
        os.system("python {0}".format(re_project_name))
    else:
        print "执行{}项目TESTNG用例".format(jenkins_name)
        xmlFileName = jenkins2xml[jenkins_name]
        print "xmlFileName--->", xmlFileName
        loop_testng(xmlFileName, testEnv='sit')


def getrealpath():
    sysstr = platform.system()
    realpath = linuxpath if sysstr == "Linux" else winpath
    return realpath


def handle_jenkin():
    result, db_number, test_apr, project_name, id, istestng, greechannel = gettestdb(jenkins_name, jenkins_number)
    if result == 0:  # 在数据库中查询不到最新的构建号
        if int(jenkins_number) > int(db_number):
            print u"构建号为{0}的{1}项目没有进行自动化测试，稍后将运行---------------->".format(jenkins_number, jenkins_name)

            # 执行用例
            run_suite(istestng, project_name, jenkins_name)
            # 执行完成后再检查一下最新的结果
            update_pushflag(jenkins_name, jenkins_number)
        elif int(jenkins_number) < int(db_number):
            print u"{1}项目回退到构建号为{0}的版本------->".format(jenkins_number, jenkins_name)
    elif result != 0:  # 查询的到版本号
        sql = "UPDATE `autotest_result`.`report_result` SET push2aliuat = '1' WHERE id = {0}".format(int(id))
        oprerate_mysql(sql)  # 跟新数据库的数据
        if int(test_apr) == 100:
            print u"执行发布到aliuat操作------------------->"
        elif greechannel == 1:
            print u"绿色通道，执行发布到aliuat操作------------------->"
        else:
            print u"该项目自动化测试未达到100%正确率，将重新运行构建号为{0}的自动化用例，请在自动化完成后重新尝试发布aliuat".format(jenkins_number)
            # 执行用例
            run_suite(istestng, project_name, jenkins_name)
            # 执行完成后再检查一下最新的结果
            update_pushflag(jenkins_name, jenkins_number)


if __name__ == '__main__':
    handle_jenkin()
