#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   ##  Copyright (c) 2012 - huangqimin <huangqimin@baidu.com>

   ##  This is used to Copy_Img to local !!!
   ##  Now just support to Copy daily && weekly 目录...
   ##  shutil.copytree 在dst存在的情况下， 会报错， 这是copytree实现的缺陷， 解决方法有两种：
       ##  一、先检测， 如果存在， 先删除， 然后拷贝...
       ##  二、重构copytree, 满足自己的需求...
   ##  后续根据需求， 可以写成， 检测有哪些， 然后供选择， 拷贝哪一个...
   ##
"""

# script: BrashMachine.py
# author: huangqimin@baidu.com

# note: 
# 1、Support for ROM has something wrong, fix it:
#    see
# 2、Add  File Named "LatestRevision", lead to Support for Master has something wrong, fix it:
#     see
# 3、Create a new file in Current Path， and copy img to this file， and before execute copy， execute delect first：
#     see

import os
import time
import shutil
import sys

def flashNS():
    global LocalPath
    adbPath = LocalPath + "/adb.exe"
    fastbootPath = LocalPath + "/fastboot.exe"
    print ">>>Flashing NS img Begin" + os.linesep
    print ">>>Today is " + time.ctime(time.time()) + os.linesep

    os.system(adbPath+" root")
    os.system(adbPath+" reboot bootloader")
    os.system(fastbootPath+" devices")
    os.system(fastbootPath+" erase cache")
    os.system(fastbootPath+" erase userdata")
    os.system(fastbootPath+" flash boot "+LocalPath+"/boot.img")
    os.system(fastbootPath+" flash system "+LocalPath+"/system.img")
    os.system(fastbootPath+" flash userdata "+LocalPath+"/userdata.img")
    os.system(fastbootPath+" reboot")
    print
    print ">>>Flashing NS img End" + os.linesep

def copyImgToLocal(fileName):
    global rom
    print ">>>Begin Copy"
    ## src
    if "" == rom:
        src = DailyPath + fileName + "/NS"
    else:
        src = DailyPath + fileName + "/G11"
    print "    src: " + src
    ## dst
    dst = LocalPath
    print "    dst: " + dst
    ## copy
    #shutil.copytree(src, "C://test/test")
    for file in os.listdir(src):
        shutil.copy(src+"/"+file, dst)
    print "\n>>>Copy Completed" + os.linesep

def fastbootNS():
    print ">>>Begin Fastboot" + os.linesep
    flashNS()
    print ">>>Fastboot Completed" + os.linesep
    time.sleep(60)
    
if __name__ == '__main__':
    date = raw_input(">>>如果您要刷指定日期的img，请输入日期，如：20120808\n>>>如果您要刷今天的img，请直接按回车\n>>>".decode('utf8').encode('gb2312')),
    print #time.strftime('%Y%m%d',time.localtime(time.time()))
    rom = raw_input(">>>如果您要刷Rom的img，请输入'Rom'\n>>>如果您要刷master的img，请直接按回车\n>>>".decode('utf8').encode('gb2312'))
    print
    direct = raw_input(">>>如果本地已经存在该日期的img，请输入'Y'\n>>>如果需要从Server端拷贝该日期的img，请直接按回车\n>>>".decode('utf8').encode('gb2312'))
    print

    #print date
    if "" == date[0]:
        ## 通过time模块， 获取当前日期（年月日）， For Example， 20120422
        today = time.strftime('%m%d',time.localtime(time.time()))
        print ">>>Today is " + time.strftime('%Y-%m-%d',time.localtime(time.time())) + os.linesep
        Year = time.localtime(time.time()).tm_year
        Month = time.localtime(time.time()).tm_mon
        Day = time.localtime(time.time()).tm_mday
        #Day = 10
    else:
        Year = date[0][0:4]
        Month = date[0][4:6]
        Day = date[0][6:8]
        print ">>>The Date You Want is " + Year+"-"+Month+"-"+Day + os.linesep

    ## daily路径
    #LocalPath = "/".join(os.getcwd().split("\\"))
    LocalPath = "/".join(sys.argv[0].split("\\")[:-1])
    #print LocalPath
    #raw_input()
    finStream = open(LocalPath+"/Path.txt", 'r')
    rowList = finStream.readlines()
    finStream.close()
    DailyPath = rowList[0].rstrip(os.linesep)
    RomPath = rowList[1].rstrip(os.linesep)
    #LocalPath = rowList[2].rstrip(os.linesep)
    #print DailyPath, RomPath, LocalPath
    #DailyPath = "//172.21.6.22/release/Yi2.1.0/daily/"
    #LocalPath = "C:\img"

    #print rom
    if "" == rom:
        pass
    else:
        DailyPath = RomPath

    #print direct
    if "" == direct:
        ## daily下面的所有的img列表
        FileList = os.listdir(DailyPath)
    
        flag = 0     # to record the num of match img
        LastFile = ""
        LastTime = 0.0
    
        if len(FileList):
            ## 遍历img列表
            for file in FileList:
                ## 判断是否是， 所想拷贝的img
                imgTime = os.stat(DailyPath+file).st_ctime

                if int(imgTime)-int(LastTime)>0:
                    LastTime = imgTime
                    LastFile = file
                else:
                    pass
                #print type(imgTime)
                #print imgTime
                imgYear = time.localtime(imgTime).tm_year
                imgMonth = time.localtime(imgTime).tm_mon
                imgDay = time.localtime(imgTime).tm_mday
                
                if int(Year)==int(imgYear) and int(Month)==int(imgMonth) and int(Day)==int(imgDay):
                    flag = 1
                    print ">>>Find the Img "+file + os.linesep
                    copyImgToLocal(file)
                    fastbootNS()
                else:
                    pass
            if 1 == flag:
                pass
            else:
                print ">>>The Newest Img is: "+LastFile
                print ">>>Which is Create at: "+time.strftime('%Y-%m-%d',time.localtime(LastTime)) + os.linesep
                copyImgToLocal(LastFile)
                fastbootNS()
        else:
            print ">>>No File in "+DailyPath + os.linesep
    else:
        print ">>>您选择了直接使用本地img进行刷机".decode('utf8').encode('gb2312') + os.linesep
        imgTime = os.stat(LocalPath+"/boot.img").st_ctime
        print ">>>本地img创建日期为：".decode('utf8').encode('gb2312')+time.strftime('%Y-%m-%d',time.localtime(imgTime)) + os.linesep
        fastbootNS()
