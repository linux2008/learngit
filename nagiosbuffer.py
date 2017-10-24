#!/usr/bin/python

import sys

from optparse import OptionParser
unit={'b':1,'k':2**10,'m':2**20,'g':2**30,'t':2**40}

def opt():
    parser=OptionParser("usage:%prog [-w Waring] [-c critical]")
    parser.add_option('-w',
                       dest='waring',
                       action='store',
                       default='100',
                       help='WARING'
                      )
    parser.add_option('-c',
                      dest='critical',
                      action='store',
                      default='50',
                      help='CRITICAL')
    option,args=parser.parse_args()
    return option,args


def getMem(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith("MemFree"):
                mem=line.split()[1].strip()
                break
    return int(mem)*1024


def scaleUnit(s):
    lastchar=s[-1]
    lastchar=lastchar.lower()
    num=float(s[:-1])
    if lastchar in unit:
        return num*unit[lastchar]
    else:
        return int(s)

def change(byte):
    for k,v in unit.items():
        num=float(byte)/v
        if 0<num<=1024:
            result='%.2f' %((num))+k.upper()
    return  result

def main():
    option,args=opt()
    w=scaleUnit(option.waring)
    c=scaleUnit(option.critical)
    print type((option.waring[-1]))
    print float(option.waring[:-1])
    mem=getMem('/proc/meminfo')
    h_read=change(mem)

    if mem>w:
        print 'ok',h_read
        sys.exit(0)
    elif c<mem<=w:
        print 'waring',h_read
        sys.exit(1)
    elif mem<c:
        print 'critical',h_read
        sys.exit(2)
    else:
        print 'unknown',h_read
        sys.exit(3)

if __name__=="__main__":
    main()
