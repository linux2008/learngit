#!/usr/bin/python

import json
import os,sys
import urllib2,urllib

dir=os.path.dirname(__file__)
conf=os.path.join(os.path.abspath(dir),'hosts')
CACHE_FILE='/var/tmp/cache.json'

def initDir():
    if not os.path.exists(conf):
         os.mkdir(conf)

temp=""" define host {
                use     linux-server
                host_name     %(hostname)s
                alias         %(hostname)s
                address       %(ip)s
}
"""
group=""" define hostgroup{ 
          hostgroup_name  %(groupname)s
          alias           %(groupname)s 
          members         %(member)s
        }
"""
def getData():
    try:
        url=urllib2.urlopen('http://192.168.235.130/getjson/')
        data1=url.read()
        with open(CACHE_FILE,'wb') as fd:
            fd.write(data1)
        return json.loads(data1)
    except:
        with open(CACHE_FILE)as fd:
            return json.load(fd)


def countDict(k,d):
   if k in d:
      d[k]+=1
   else:
      d[k]=1

def paserData(data):
    dic={}
    con=''
    gcon=''
    for i in data:
        groupname=i['groupname']
#        members=[]
        for a in i['member']:
            hostname=a['hostname']
#            members.append(hostname)     
            countDict(hostname,dic)
            if dic[hostname]<2:       
                con+=temp %a

#        gcon+=group %{'groupname':groupname,'member':''.join(members)}
        gcon+=group %{'groupname':groupname,'member':hostname}
    dir_host=os.path.join(conf,'host.cfg')
    dir_group=os.path.join(conf,'group.cfg')
    writefile(dir_host,con)
    writefile(dir_group,gcon)

def writefile(f,s):
    with open(f,'w') as fd:
        fd.write(s)

if __name__=="__main__":
    initDir()
    data=getData()
    paserData(data)
