# coding:utf-8
"""
定时任务，运行新框架用例
"""
import jenkins

jenkins_config = {"jenkins_url": "http://jenkins.immd.cn/", "username": "lingbo.wang",
                  "password": "yourtoken"}

def loop_testng(xmlFileName='testng-sit.xml', testEnv='sit'):
    server = jenkins.Jenkins(jenkins_config["jenkins_url"], username=jenkins_config['username'],
                             password=jenkins_config["password"])
    server.build_job('IntegrationTest', {'xmlFileName': xmlFileName, 'testEnv': testEnv})


if __name__ == '__main__':
    loop_testng()