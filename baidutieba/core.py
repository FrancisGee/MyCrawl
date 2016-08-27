__author__='GYK'
# -*- codding:utf-8 -*-
import urllib
import urllib2
import re

#Handle the page tags(wash the dta)
class Tool():

    #remove img tag by 7 long space
    removeImg=re.compile('<img.*?>| {7}|')
    #remove hyperlink tag
    removeAddr=re.compile('<a.*?>|</a>')
    #replace linebreak tag to \n
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    #replace tab tag  <td>  to \t
    replaceTD=re.compile('<td>')
    #replace the paragraph head to \n with 2 space
    replacePara=re.compile('<p.*?>')
    #replace linebreak or double linebreak to \n
    replaceBR=re.compile('<br><br>|<br>')
    #remove other tags
    removeExtraTag=re.compile('<.*?>')

    def replace(self,x):
          x=re.sub(self.removeImg ,"",x)
          x=re.sub(self.removeAddr,"",x)
          x=re.sub(self.replaceLine,"\n",x)
          x=re.sub(self.replaceTD,"\t",x)
          x=re.sub(self.replacePara,"\n  ",x)
          x=re.sub(self.replaceBR,"\n",x)
          x=re.sub(self.removeExtraTag,"",x)
          #strip() to remove front and back extra content
          return x.strip() 

#Baidu tieba class
class BDTB:

    #init ,pass the baseurl ,if only see lz parameter
    def __init__(self,baseUrl,seeLZ):
        self.baseURL=baseUrl
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()

    #pass the Page index, crawl the post html in the page
    def getPage(self,pageNum):
        try:
            url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
        #    print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                 print "connect to baidu tieba failed, the reason is that",e.reason
                 return None
    #get the title of the post
    def getTitle(self):
        page=self.getPage(1)
        pattern=re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result=re.search(pattern,page)
        if result:
             print result.group(1)
             return result.group(1).strip()
        else:
             return None
    #get total reply posts
    def getPageNum(self):
        page=self.getPage(1)
        pattern=re.compile('<li class="l_reply_num.*?<span.*?>(.*?)</span>',re.S)
        result=re.search(pattern,page)
        if result:
             print result.group(1)
             return result.group(1).strip()
        else:
             return None
    def getContent(self,page):
       # page=self.getPage(pageIndex)
        pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items=re.findall(pattern,page)
        floor=1
        for item in items:
            print floor,"Floor---------------------------------------------------------------------------------------------------------------\n"
         
            print self.tool.replace(item)
            floor+=1 


baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseURL,1)
#bdtb.getPage(1)

bdtb.getContent(bdtb.getPage(1))
