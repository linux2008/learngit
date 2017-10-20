#!/usr/bin/python

from subprocess import PIPE,Popen
import re

def get():
    p=Popen(['ifconfig'],stdout=PIPE)
    data=p.stdout.read().split('\n\n')
    return [i.strip() for i in data if not i.startswith('lo') and i]


def getip(data):
    data=get()
    dic={}
    devname=re.compile(r'(docker|eth|br|bond|em)[\d:]+',re.M)
    devmac=re.compile(r'(\w+:){5}\w+',re.M)
    devip=re.compile(r'([\d+]+\.)+[\d]+',re.M)
    for i in data:
        name=devname.search(i).group()
        mac=devmac.search(i).group()
        ip=devip.search(i).group()
 
       dic.update({name:[mac,ip]})
    return dic
if __name__=='__main__':

    data=get()
    print getip(data)
