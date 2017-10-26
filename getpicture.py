#!/usr/bin/python


import urllib,urllib2
import re
def get(url):
    page=urllib2.urlopen(url)
    return page.read()

def image(html):
    r=re.compile(r'<img class="BDE_Image" src="(.*?)"')
    images=r.findall(html)
    i=1
    for url in images:
        print url
        urllib.urlretrieve(url,filename="%s.jpg" %i)
        i+=1
if __name__=="__main__":
   
    url='http://tieba.baidu.com/p/4229162765'
    page=get(url)
    print image(page)
    
