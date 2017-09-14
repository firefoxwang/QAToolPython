# -*- coding:utf-8 -*-
import logging

import numpy as np
# 导入图表库以进行图表绘制
import matplotlib.pyplot as plt
import pymysql

mysql_config = {"host": "99.48.66.40",
                "user": "wanglingbo",
                "passwd": "Wanglingbo@123",
                "charset": "utf8",
                }


def __oprerate_mysql(sql, mysql_config=mysql_config):
    conn_mysql = pymysql.connect(host=mysql_config["host"], user=mysql_config["user"], passwd=mysql_config["passwd"],
                                 charset="utf8")
    return_info = None

    try:
        if 'select' in sql.lower():
            cursor = conn_mysql.cursor()
            cursor.execute(sql)
            return_info = cursor.fetchall()
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


def handle_jenkindb(jenkins_name, period):
    """

    :param jenkins_name: jenkins项目的名字
    :param period: 入参为想要获取的时间范围,必须传的参数,2天，3天，从0开始数
    :return:返回自动化的时间跟通过率，字典格式
    """
    result_apr = []
    result_time = []
    sql = "SELECT start_time,test_apr FROM `autotest_result`.`report_result` WHERE DATE_SUB(CURDATE(), INTERVAL {0} DAY) <= DATE(start_time) AND jenkins_name = '{1}' AND push2aliuat = '1' ORDER BY start_time;".format(
        period, jenkins_name)
    # sql = "SELECT start_time,test_apr FROM `autotest_result`.`report_result` WHERE DATE_SUB(CURDATE(), INTERVAL {0} DAY) <= DATE(start_time) AND jenkins_name = '{1}' ORDER BY start_time;".format(
    #     period, jenkins_name)  # 一周的用例通过率
    result = __oprerate_mysql(sql)
    if result != ():  # result查不到值
        for i in result:  # 分别存储对应的值
            result_time.append(i[0].strftime("%m-%d %H:%M"))  #如果是所有的用例 就直接看天数
            # result_time.append(i[0].strftime("%d"))
            result_apr.append(i[1])
    else:
        logging.info("the result is None")
    return tuple(result_time), tuple(result_apr)


def showpic(jenkins_name, period):
    result_time, result_apr = handle_jenkindb(jenkins_name, period)
    loandata = result_apr

    # 设置日期字段issue_d为loandata数据表索引字段
    # 按月对贷款金额loan_amnt求均值，以0填充空值
    loan_plot = loandata

    plt.rc('font', size=15)
    # 创建一个一维数组赋值给a
    a = np.array(range(len(result_apr)))
    # 创建折线图，数据源为按月贷款均值，标记点，标记线样式，线条宽度，标记点颜色和透明度
    plt.plot(loan_plot, 'g^', loan_plot, 'g-', color='#99CC01', linewidth=3, markeredgewidth=3,
             markeredgecolor='#99CC01',
             alpha=0.8)
    # 添加x轴标签
    plt.xlabel(u'自动化测试日期（/日）')
    # 添加y周标签
    plt.ylabel(u'自动化通过率(%)')
    # 添加图表标题
    plt.title(u'{}项目自动化{}天结果图表'.format(jenkins_name,period+1))
    # 添加图表网格线，设置网格线颜色，线形，宽度和透明度
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
    # 设置数据分类名称
    plt.xticks(a, result_time)
    # 输出图表
    plt.show()


if __name__ == '__main__':
    showpic(jenkins_name="cms-manager-web", period=4)
