# -*-coding: UTF-8 -*-

import paramiko

ssh = paramiko.SSHClient
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip='10.0.10.57', port=22, username='root',password='shinemo123')
stdin, stdout, strerr = ssh.exec_command('ls /usr/local')
result = stdout.read()

ssh.close()