# -*-coding:UTF-8 -*-
#! /bin/env python3

# fabric模块基于fabric3这个包，如果pip安装的是fabric这个包，导入的时候会有问题
from fabric.api import *
from datetime import datetime as d
import os, sys
import uuid

env.user = 'root'
env.password = 'shinemo123'
env.host = ['10.0.10.72', '10.0.10.73']

now_time = d.now().strftime('%Y%m%d%H%M%S')
deploy_target = '/tmp/deploy_' + now_time + '.tar.gz'

def pack():
    """定义一个打包任务"""
    rechk_list = []
    chk_list = []
    handlefile = '/tmp/deploy_target'
    for targetFile in open(handlefile):
        if not os.path.exists(targetFile.strip()):
            rechk_list.append(targetFile.strip())
        else:
            chk_list.append(targetFile.strip())
    if len(rechk_list) > 0:
        print("{} is not found, Please check, and make sure target file or target path can be found by the program!" .format([x for x in rechk_list]))
        exit(1)
    else:
        if os.path.exists(deploy_target):
            print("{} is exsited, program will delete it!" .format(deploy_target))
            lcoal('rm -f {}' .format(deploy_target))
            print("The packaging job begins to execute...")
            local('tar -czvf {} {}' .format(depoly, ' '.join(chk_list)))
        else:
            local('tar -czvf {} {}'.format(deploy_target, ' '.join(chk_list)))


def deploy():
    base_path = '/tmp'
    current_day = d.now().strftime('%Y%m%d')
    uid = str(uuid.uuid1()).split('-')[0]
    remote_tmp_path = base_path + '/' + current_day + '_' + uid
    remote_deploy_path = sys.argv[1]
    run('mkdir {}' .format(remote_tmp_path))
    put('{}' .format(deploy_target) , '{}' .format(remote_tmp_path))
    with cd('{}' .format(remote_tmp_path)):
        run('tar zxvf {} -C {}' .format(remote_tmp_path,deploy_target, remote_deploy_path))

if __name__ == '__main__':
    print('The automatic deployment program starts executing...')
    pack()
    deploy()

