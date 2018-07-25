# -*-coding:UTF-8 -*-
#! /bin/env python3

# fabric模块基于fabric3这个包，如果pip安装的是fabric这个包，导入的时候会有问题'
from fabric.api import *
from datetime import datetime as d
import os, sys

env.user = 'root'
env.password = 'shinemo123'
env.host = ['10.0.10.72', '10.0.10.73']

def pack():
    '定义一个打包任务'
    rechk_list = []
    chk_list = []
    deploy = sys.argv[1]
    handlefile = '/tmp/deploy_target'
    for tp in open(handlefile):
        if not os.path.exists(tp.strip()):
            rechk_list.append(tp.strip())
        else:
            chk_list.append(tp.strip())
    if len(rechk_list) > 0:
        print("{} is not found, Please check, and make sure target file or target path can be found by the program!" .format([x for x in rechk_list]))
        exit(1)
    else:
        if os.path.exists(deploy):
            print("{} is exsited, program will delete it!" .format(deploy))
            lcoal('rm -f {}' .format(deploy))
            print("The packaging job begins to execute...")
            local('tar -czvf {} {}' .format(depoly, ' '.join(chk_list)))
        else:
            local('tar -czvf {} {}'.format(deploy, ' '.join(chk_list)))


if __name__ == '__main__':
    pack()
