# -*- coding:UTF-8 -*-
# !/bin/env python3

from fabric.api import *
import os, sys

env.user = 'admin'
env.password = 'shinemo123'
env.hosts = []

deployTarget = sys.argv[1]
deployTarget = deployTarget.lower()
localPath = '/data/deploy'
PrjPackage = deployTarget + '.war'
deployPackagePath = localPath + '/' + PrjPackage

@hosts('10.0.10.64','10.0.10.69','10.0.10.78')
def collectJavaSrv():
    '''
    遍历各java服务器上的以tomcat方式启动的java服务，用字典来存放数据
    :return:字典
    '''
    srvPath = run("ps -ef |grep java |grep -v grep |awk '{print $9}' |awk -F '.' '{print $5}' |awk -F '=' '{print $2}' \
                  |awk -F 'conf' '{print $1}'")
    handlepath = srvPath.splitlines()
    srvDict = {}
    ip = run("ip a |grep inet |grep -v '127.0.0.1' |awk '{print $2}' |awk -F '/' '{print $1}'")
    for i in handlepath:
        appPath = i + 'webapps/'
        Project = run('cd {} && ls |grep -E -v "war|properties"' .format(appPath))
        handleProject = Project.splitlines()
        for j in handleProject:
            srvDict[j] = {'host':ip, 'path':i}
    return srvDict

def dict_get(dict, objkey):
    '''
    处理字典数据
    :param dict: collectJavaSrv返回的数据
    :param objkey: 要部署的项目
    :return: 如果找到执行项目，返回该项目的部署ip和war包路径，否则返回提示信息
    '''
    handledict = {}
    for host, prjinfo in dict.items():
        for key,value in prjinfo.items():
            if key == deployTarget:
                handledict[key] = value
                return handledict
    print('未找到该项目，请确认该项目之前是否已部署!')
    exit(1)

def getRemoteInfo():
    for prjname, info in ret.items():
        for host, ip in info.items():
            if host == 'host':
                Host = ip

    for prjname, info in ret.items():
        for path, pathname  in info.items():
            if path == 'path':
                Path = pathname
    return Host, Path

def deployPrj():
    '''
    部署项目，并重启进程
    '''
    env.user = 'admin'
    env.password = 'shinemo123'
    env.hosts = [remotehost]
    remoteAppPath = remotepath + 'webapps/'
    print("删除旧版本{}" .format(PrjPackage))
    run("cd {} && rm -f {}" .format(remoteAppPath, PrjPackage))
    print("上传新版本war包...")
    put(deployPackagePath,remoteAppPath)
    run("chown -R admin.admin {}" .format(remotepath))
    print("重启进程...")
    run("ps -ef |grep %s |grep -v grep |awk '{print $2}' |xargs kill -9" % (remotepath))
    run("cd {}bin && ./startup.sh" .format(remotepath), pty=False)
    processNum = run("ps -ef |grep {} |grep -v grep |wc -l" .format(remotepath))
    if processNum == "0":
        print("Tomcat进程已kill，但未重启！请重新执行此脚本！")
    else:
        print("部署完成！")


if __name__ == '__main__':
    with settings(hide('running','stdout','stderr','warnings','everything')):
        print("开始执行...")
        results = execute(collectJavaSrv)
        ret = dict_get(results, deployTarget)
        remotehost, remotepath = getRemoteInfo()
        env.hosts.append(remotehost)
        execute(deployPrj)