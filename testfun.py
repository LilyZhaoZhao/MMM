#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

def myfun():
    x=2
    print 'x in myfun: ', x

def myfun2():
    x=3
    print 'x in myfun: ', x


if __name__=="__main__":
    x = 0
    print x

    myfun()
    myfun2()
    print x
