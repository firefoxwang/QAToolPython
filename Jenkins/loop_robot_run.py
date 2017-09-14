# -*- coding:utf-8 -*-

from concurrent import futures
import os
import time
import sys
sys.path.append("/home/user/execution/Public/Soraka")
from run_config import project_config

def run(project_config):
    # 循环执行所有项目
    project=project_config.keys()[0]
    os.system(r'python /home/user/execution/Public/Soraka/robot_run.py {0}'.format(project.encode('utf-8')))

if __name__=='__main__':
    startFrom = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    with futures.ProcessPoolExecutor(max_workers=10) as executor:
        executor.map(run, project_config)
    endTo = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "任务持续：{0}-{1}".format(startFrom, endTo)
