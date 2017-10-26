#!/usr/bin/python


from optparse import OptionParser
from subprocess import Popen,PIPE
import shlex
import datetime
import operator
import sys
import re
Reg=re.compile('(?P<logtime>\w+)\s(?P<hostname>[\d]+\s[\d+:]{8})\s(?P<program>\w+\s\w+\[\d+\]\:)(?P<msg>.*)')

MONTH={
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12
   }

def opt():
    parser=OptionParser("usage:%prog -w[ waring ] -c[ critical ]")
    parser.add_option('-w',
                        dest='waring',
                        action='store',
                        default='5',
                        help='only waring'
                        )
    parser.add_option('-c',
                        dest='critical',
                        action='store',
                        default='10',
                        help='only critical')
    options,args=parser.parse_args()

    return options,args



def parseFile(f,n):
    cmd='tail -n %s %s ' %(n,f)
    p=Popen(shlex.split(cmd),stdout=PIPE,stderr=PIPE)
    stdout,stderr=p.communicate()
    return stdout


def getTime(line):
    now=datetime.datetime.now()
    month,day,time=line.split()[:3]
    hour,minute,second=[int(i) for i in time.split(':')]
    logtime=datetime.datetime(now.year,MONTH[month],int(day),hour,minute,second)
    return logtime
    
def parseLog(data):
    dic={}
    now=datetime.datetime.now()
    ten_ago=now-datetime.timedelta(minutes=60)
    data=[line for line in data.split('\n') if line]
    for line in data:
       logtime=getTime(line)
       if logtime>ten_ago:
           match=Reg.search(line)
           if match:
               match_dic=match.groupdict()
               k=str(logtime)+''+match_dic['program']
               if 'info' in match_dic['msg'].lower():
                   countDic(k,dic)
    return dic


def countDic(k,d):
    if k in d:
       d[k]+=1
    else:
       d[k]=1

def main():
    options,args=opt()
    w=int(options.waring)
    c=int(options.critical)
    line=c*600    
    data=parseFile('/var/log/messages',20)
    dic=parseLog(data)
    sorted_dic=sorted(dic.iteritems(),key=operator.itemgetter(1),reverse=True)[0]
    num=int(sorted_dic[1])
    if num < w:
        print 'ok',sorted_dic
        sys.exit(0)
    elif c>num>=w:
         print 'waring',sorted_dic
         sys.exit(0)
    elif num>=c:
         print 'critical',sorted_dic
         sys.exit(2)
    else:
         print 'unknown',sorted_dic
         sys.exit(3)  


if __name__=="__main__":
    print main()
