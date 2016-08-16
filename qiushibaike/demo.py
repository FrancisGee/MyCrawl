
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

opener=urllib2.build_opener()
page=1

url='http://www.qiushibaike.com/hot/page/'+str(page)
user_agent='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/40.0.2214.111 Chrome/40.0.2214.111 Safari/537.36'
headers={'User-Agent':user_agent}


opener.addheaders=headers.items()

try:
    request=urllib2.Request(url)
    response=opener.open(url)
    
    content= response.read().decode('utf-8')
     # pattern=re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>',re.S)
    pattern=re.compile('<div class="author clearfix">.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>',re.S)
    items=re.findall(pattern,content)
    for item in items:
               print("Author: "+item[0])
               print("Content: "+item[1])
               print("Favorite: "+item[2])
               print("Comments: "+item[3])
except urllib2.URLError,e:
    if hasattr(e,"code"):
       print e.code
    if hasattr(e,"reason"):
       print e.reason
