#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 26 Nov 2017 08:12:18 PM CST
# Description: Given a .srt file in dos format with correct content,
#              but incorrect timestamp and index. Corret them.
#########################################################################

def int_2_bytes(i):
    l = []
    while i > 0:
        l.append(i%10)
        i = i//10
    l.reverse()
    for j in range(len(l)):
        l[j] = ord('0')+l[j]
    return bytes(l)

def time_minus_base(now, base):

    def __time(s):

        hh = int(s[:2])
        mm = int(s[3:5])
        ss = int(s[6:8])
        ms = int(s[9:])
        return hh*3600+mm*60+ss+ms/1000

    t = __time(now) - __time(base)

    ms = int(t*1000%1000)
    ss = int(int(t)%60)
    mm = int((int(t)-ss)%3600//60)
    hh = int(t-ss-60*mm)//3600
    return "{:02}:{:02}:{:02},{}".format(hh,mm,ss,ms)

def f():
    f = open('str2.srt','rb') # FIXME
    lines = f.readlines()
    index = 1
    output = b''
    counter = 0
    start_time = '00:55:49,000' #FIXME
    for line in lines:

        if (counter == 0):
            line = int_2_bytes(index)+line[line.find(b'\r'):]
            index += 1

        if (counter == 1):
            line = line.rstrip()
            t1 = line[:line.find(b' ')]
            t1 = time_minus_base(t1,start_time)
            t2 = line[line.find(b'>')+2:]
            t2 = time_minus_base(t2,start_time)
            line = bytes(t1,'ascii')+b" --> "+bytes(t2,'ascii')+b'\r\n'

        if (line == b'\r\n'):
            counter = -1

        output += line
        print (line)
        counter += 1

    return output

