#!/usr/bin/python
#encoding:utf8
import requests
import re

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"}

session=requests.session()

params={
        "language":"-1",
        "style":"-1",
        "df":"mail126_letter",
        "from":"web",
        "allssl":"true",
        "race":"-2_-2_-2_db",
        "net":"failed",
        "iframe":"1",
        "product":"mail126",
        "url2":"http://mail.126.com/errorpage/error126.htm", 
        "passtype":"0",
        "savelogin":"0"}

data={"username":"xiaofu02@126.com",
      "password":"93b0ecb5d87157542cb676fa79522493"}

url="https://mail.126.com/entry/cgi/ntesdoor?"
login=session.post(url=url,data=data,params=params,headers=headers)
re_url=re.compile(r'href= "(.*?)"')
re_url1=re_url.findall(login.text)[0]

print re_url1
print login.url
print login.status_code
print login.text
