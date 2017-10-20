#!/usr/bin/python

from subprocess import Popen,PIPE

def hostpipe():

    p=Popen('cat /etc/sysconfig/network',stdout=PIPE,shell=True)
    data=p.stdout.readlines()
    return data

def ippipe():
    p=Popen(['ifconfig'],stdout=PIPE)
    data=p.stdout.read()
    return [i for i in data.split('\n\n') if not i.startswith('docker0') and i]

def dmipipe():
    p=Popen(['dmidecode'],stdout=PIPE)
    data=p.stdout
    return data

def osverpipe():
     p=Popen(['cat','/etc/issue'],stdout=PIPE)
     data=p.stdout.readlines()
     return data

def cpupipe():
    p=Popen(['cat','/proc/cpuinfo'],stdout=PIPE)
    data=p.stdout.read()
    return data

def mempipe():
    p=Popen(['cat','/proc/meminfo'],stdout=PIPE)
    data=p.stdout.read()
    return data

def getmem(data):
    dic={}
    data=mempipe()
    for i in data.split('\n'):
        if i.startswith('MemTotal'):
            dic['memory']=i.split(':')[1].strip()
    return dic

def getcpu(data):
    dic={}
    data=cpupipe()
    for i in data.split('\n'):
        if i.startswith('processor'):
            dic['cpu_num']=i.split(':')[1].strip()
        if i.startswith('model name'):
            dic['cpu_model']=i.split(':')[1][:9].strip()
    return dic

def getosver(data):
    dic={}
    data=osverpipe()
    osver=[i.strip() for i in data]
    dic['osver']=osver[0]
    return dic

def getdmi(data):
    data=dmipipe()
    lines=[]
    a=True
    dic={}
    while a:
        datas=data.readline()
        if datas.startswith('System Information'):
            while True:
                line=data.readline()
                if line=='\n':
                    a=False
                    break
                else:
                    lines.append(line)
    message=[ i.strip() for i in lines]
    dic['vender']=message[0].split(':')[1]
    dic['product']=message[1].split(':')[1]
    dic['sn']=message[3].split(':')[1][10:30]
    return dic


def gethostname(data):
    dic={}
    dic['hostname']=data[1].split('=')[1].strip()
    return dic

def getip(ip):
    ip=ippipe()
    dic={}
    for i in ip:
        mc=i.split('\n\n')
        devname=mc[0].split()[0]
        ip=mc[0].split('\n')[1].split()[1].split(':')[1]
        dic[devname]=ip
    return dic

if __name__=='__main__':
    dic={}
    data=hostpipe()
    name= gethostname(data)

    ip=ippipe()
    ipa=getip(ip)

    data=dmipipe()
    getd=getdmi(data)

    data=osverpipe()
    geto=getosver(data)

    data=cpupipe()
    getc=getcpu(data)

    data=mempipe()
    getm=getmem(data)

    dic.update(name)
    dic.update(ipa)
    dic.update(getd)
    dic.update(geto)
    dic.update(getc)
    dic.update(getm)
    print dic
