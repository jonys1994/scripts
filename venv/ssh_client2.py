# -*-coding: UTF-8 -*-

import paramiko
import os

testfile='/data/devops/scripts/test'

transport = paramiko.Transport('10.0.10.57', 22)
transport.connect(username='root',password='shinemo123')

ssh = paramiko.SSHClient()
ssh._transport = transport
stdin, stdout, stderr = ssh.exec_command('df')

if not os.path.exists(testfile):
    os.system(r'touch {}' .format(testfile))

with open(testfile,'r+') as f:
    print(stdout.read(), f)
transport.close()