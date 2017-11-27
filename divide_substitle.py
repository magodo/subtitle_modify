#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 26 Nov 2017 08:12:18 PM CST
# Description: Given a .srt file in dos format with correct content,
#              but incorrect timestamp and index. Corret them.
#########################################################################

try:
    import chardet
except ImportError as e:
    print("Need module: chardet")
    raise e

import sys
import argparse

def time_shift(now, shift):

    def __time(s):

        hh = int(s[:2])
        mm = int(s[3:5])
        ss = int(s[6:8])
        ms = int(s[9:])
        return hh*3600+mm*60+ss+ms/1000

    t = __time(now) - __time(shift)

    ms = int(t*1000%1000)
    ss = int(int(t)%60)
    mm = int((int(t)-ss)%3600//60)
    hh = int(t-ss-60*mm)//3600
    return "{:02}:{:02}:{:02},{}".format(hh,mm,ss,ms)

def convert(source, shift, dest = 'output.srt'):

    # Detect the encoding of the input source file since we'll open it in "text" mode.
    # Also detect the line ending of it since we'll keep it (otherwise, file opened in
    # "text" mode for write will depend on os.linesep).
    with open(source, 'rb') as f:

        # detect line ending
        first_line = f.readline()
        if first_line.endswith(b'\r\n'):
            ending = '\r\n'
        elif first_line.endswith(b'\r'):
            ending = '\r'
        elif first_line.endswith(b'\n'):
            ending = '\n'
        else:
            # just guess
            print("Line ending detection failed, guess it is '\n'...")
            ending = '\n'

        # detect file encoding
        raw_content = b''.join([first_line]+f.readlines())
        encoding = chardet.detect(raw_content)['encoding']

    # detect the line ending of the input source file


    # now begins real work
    index = 1
    counter = 0
    new_content = ''
    with open(source, 'r', encoding = encoding) as f:
        for line in f:

            # update index
            if counter == 0:
                line = str(index) + line[line.find('\n'):]
                index += 1

            # update the timestamp
            if counter == 1:
                t1 = time_shift(line[:line.find(' ')], shift)
                t2 = time_shift(line[line.find('>')+2:-1], shift)
                line = t1 + " --> " + t2 + '\n'

            # end of a subtitle section
            if line == '\n':
                counter = -1

            line = line.replace('\n', ending)
            new_content += line
            counter += 1

    # write out
    with open(dest, 'w', encoding=encoding, newline='') as f:
        f.write(new_content)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help = 'input subtitle file')
    parser.add_argument('-s', '--shift', help = 'shift time, normally equals to the length of last video(s) (e.g. 00:55:49,000)')
    parser.add_argument('-o', '--output', help = 'output subtitle file', default = 'output.srt')

    args = parser.parse_args()

    sys.exit(convert(args.input, args.shift, args.output))
