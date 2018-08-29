# -*-coding: UTF-8 -*-
#! /bin/env python

import redis
from redis.sentinel import Sentinel

authPasswd = 'F6D098YDDE3DCNNIEII2MCB7M7OGR2G6K'
key = 'foo'
value = 'bar'
sentinel1 = Sentinel([('192.168.22.119', 26379),
                     ('192.168.28.179', 26379)
                     ],
                    socket_timeout=0.5)

master = sentinel1.discover_master('mymaster')
print(master)

slave = sentinel1.discover_slaves('mymaster')
print(slave)

master = sentinel1.master_for('mymaster', socket_timeout=0.5, password='F6D098YDDE3DCNNIEII2MCB7M7OGR2G6K', db=15)
w_ret = master.set({}, {} .format(key,value))

slave = sentinel1.slave_for('mymaster', socket_timeout=0.5, password='F6D098YDDE3DCNNIEII2MCB7M7OGR2G6K', db=15)
r_ret = slave.get({} .fomat(key))
print(r_ret)