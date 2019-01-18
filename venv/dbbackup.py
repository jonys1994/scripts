# -*- coding: UTF-8 -*-
#! /bin/env python

import subprocess
from datetime import datetime as datetime2
import datetime
import os, sys
import logging

backupuser = 'backup'
backuppasswd = 'shinemo123'
fullbackupdir = '/data/dbbackup/full-backup/'
incrementalbackupdir = '/data/dbbackup/incremental-backup/'
dbconf = '/database/3306/my.cnf'
nowdate = datetime2.today()
lastfullbackupdate = (nowdate + datetime.timedelta(-7)).date()
lastincrementalbackupdate = (nowdate + datetime.timedelta(-1)).date()
fullbackupcommand = 'innobackupex --defaults-file={} --user={} --password={} {}'
incrementalbackupcommand = 'innobackupex --defaults-file={} --user={} ' \
                           '-password={} --incremental-basedir={} --incremental {}'
filterfilecommd = "ls -l %s |grep %s |awk '{print $9}'"


logger = logging.getLogger("mainModle")
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('/opt/dbbackup/database_backup.log')
handler.setLevel(level=logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# full backup task function
def fullbackup():
    """
    :return: 0, -1，-2 or -3
    """
    retcode = subprocess.run('ls {} |grep {} ' .format(fullbackupdir, lastfullbackupdate), shell=True).returncode
    if retcode == 0:
        logger.info("A full backup file completed a week ago has been found, start the full backup task.")
        attempts = 0
        while attempts < 3:
            full_retcode = subprocess.run(fullbackupcommand.format(
                dbconf, backupuser, backuppasswd, fullbackupdir), shell=True).returncode
            if full_retcode == 0:
                logger.info("The full backup task has been completed.")
                # 非首次全备完成
                return 0
            logger.warning("Full backup task is failed, try again.")
            attempts += 1
        logger.error(
            "Full backup task has been failed three times, "
            "please check the mysql , backup tools or this scripts!")
        # 非首次全备失败
        return -1
    else:
        if not os.listdir(fullbackupdir):
            logger.info("First full backup task start.")
            attempts = 0
            while attempts < 3:
                full_retcode = subprocess.run(fullbackupcommand.format(
                    dbconf, backupuser, backuppasswd, fullbackupdir), shell=True).returncode
                if full_retcode == 0:
                    logger.info("The full backup task has been completed.")
                    # 首次全备完成
                    return 0
                logger.warning("Full backup task is failed, try again.")
                attempts += 1
            logger.error(
                "The first full backup task has been failed three times, "
                "please check the mysql , backup tools or this scripts!")
            # 首次全备失败,删除全备目录备份残留信息，程序退出
            subprocess.run("cd {} && rm -rf *" .format(fullbackupdir), shell=True)
            exit(1)
        logger.info("The full backup file a week ago was not found, The full backup task will exit.")
        # 未到全备日期，无需全备
        return -2

# incremental backup task function
def incrementalbackup(fullretcode):
    """
    :param fullretcode: fullbackup return code
    :return: 0 or -1
    """
    if fullretcode == -1:
        logger.info(
            "Because of the full backup failed just now, "
            "the incremental backup will be based on the last incremental backup file.")
        incrementalbaseddir = subprocess.run(filterfilecommd % (
            incrementalbackupdir, lastincrementalbackupdate), shell=True).stdout
        attempts = 0
        while attempts < 3:
            incremental_retcode = subprocess.run(incrementalbackupcommand.format(
                dbconf, backupuser, backuppasswd, incrementalbaseddir, incrementalbackupdir), shell=True).returncode
            if incremental_retcode == 0:
                logger.info("The incremental backup task has been completed.")
                return 0
            logger.warning("Incremental backup task is failed, try again.")
            attempts += 1
        logger.error(
            "Incremental backup task has been failed three times, "
            "please check the mysql, backup tools or this scripts, program will exit!")
        exit(1)
    # 无需全备，直接增备
    elif fullretcode == -2:
        logger.info(
            "Today is not required to perform full backup tasks, "
            "the incremental backup will be based on the last incremental backup file.")
        isyesterdayfullbackup = subprocess.run(filterfilecommd % (
            fullbackupdir, lastincrementalbackupdate), shell=True)
        if isyesterdayfullbackup.returncode == 0:
            incrementalbaseddir = isyesterdayfullbackup.stdout
            print(incrementalbaseddir)
            attempts = 0
            while attempts < 3:
                incremental_retcode = subprocess.run(incrementalbackupcommand .format(
                    dbconf, backupuser, backuppasswd, incrementalbaseddir, incrementalbackupdir), shell=True).returncode
                if incremental_retcode == 0:
                    logger.info("The incremental backup task has been completed.")
                    return 0
                logger.warning("Incremental backup task is failed, try again.")
                attempts += 1
            logger.error(
                "Incremental backup task has been failed three times, "
                "please check the mysql, backup tools or this scripts, program will exit!")
            exit(1)
        incrementalbaseddir = subprocess.run(
            filterfilecommd % (incrementalbackupdir, lastincrementalbackupdate), shell=True).stdout
        attempts = 0
        while attempts < 3:
            incremental_retcode = subprocess.run(incrementalbackupcommand.format(
                dbconf, backupuser, backuppasswd, incrementalbaseddir, incrementalbackupdir), shell=True).returncode
            if incremental_retcode == 0:
                logger.info("The incremental backup task has been completed.")
                return 0
            logger.warning("Incremental backup task is failed, try again.")
            attempts += 1
        logger.error(
                "Incremental backup task has been failed three times, "
                "please check the mysql, backup tools or this scripts, program will exit!")
        exit(1)
    logger.info("A full backup file completed just now has been found, this incremental backup task will be skipped.")
    return 0

if __name__ == '__main__':
    fullretcode = fullbackup()
    incrementalbackup(fullretcode)