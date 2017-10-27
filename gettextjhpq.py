#!/usr/bin/python
#encoding:utf8

import urllib,urllib2
import re
import sys

def getpage(page_num=1):
    url='https://www.qiushibaike.com/8hr/page/'+str(page_num)

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}

    request=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(request)
    html=response.read()
    return html

def getpagehtml(page_num=1):
    html=getpage(page_num)
    re_page=re.compile(r'<div class="author.*?>.*?<a.*?<img .*?>.*?</a>.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<div class="stats">.*?<i class="number">(\d+)</i>',re.S)

    #re_page=re.compile(r'<div class="author.*?>.*?<a.*?<img .*? alt="(.*?)">.*?</a>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<div class="stats">.*?<i class="number">(\d+)</i>',re.S)
    items=re_page.findall(html)
    page_contents=[]
    replaceBR=re.compile(r'<br/>')
    for item in items:
        content=item[1]
        content=replaceBR.sub('\n',content)
        page_contents.append([page_num,
                             item[0].strip(),
                             item[1].strip(),
                             item[2].strip()])

    return page_contents

def getonestory(page_contents):
    for story in page_contents:
        input=raw_input()
        if input=='Q' or input=='q':
            sys.exit()
    
        print "第%s页\t发布人:%s\t赞:%s\n%s\n" %(story[0],story[1],story[3],story[2])


if __name__=="__main__":
    print "正在读取段子，按回车看新段子，退出(Q/q)"
    page_num=1
    while True:
        page=getpagehtml(page_num)
        getonestory(page)
        page_num+=1



