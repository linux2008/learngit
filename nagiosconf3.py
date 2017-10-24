#!/usr/bin/python

import json
import os,sys
import urllib2,urllib

dir=os.path.dirname(__file__)
conf=os.path.join(os.path.abspath(dir),'hosts')

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
group=""" define service{ 
          hostgroup_name  %(groupname)s
          alias           %(groupname)s 
          members         %(member)s
        }
"""
def getData():
    url=urllib2.urlopen('http://192.168.235.130/getjson/')
    data=json.loads(url.read())
    return data

def paserData(data):

    con=''
    gcon=''
    for i in data:
        groupname=i['groupname']
#        members=[]
        for a in i['member']:
            hostname=a['hostname']
#            members.append(hostname)            
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
