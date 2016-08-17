# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

#the class of qiushibaike
class QSBK:
	def __init__(self):
	  self.pageIndex=1
	  self.user_agent='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/40.0.2214.111 Chrome/40.0.2214.111 Safari/537.36'
          #initialize headers
	  self.headers={'User-Agent': self.user_agent}
          #to store "duanzi",every item is one page of "duanzi"
	  self.stories=[]
          #judge wheather the crawl continue
          self.enable=False
	#pass the PageIndex to crawl the page html
	def getPage(self,pageIndex):
	  try:
		url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
                request=urllib2.Request(url,headers=self.headers)
       	 	response=urllib2.urlopen(request)
                #encoding the page into utf-8
  		pageCode=response.read().decode('utf-8')
		return pageCode
	  except urllib2.URLError,e:
	        if hasattr(e,"reason"):
		    print u"connect to www.qiushibaike.com failed,the reason is:",e.reason
		    return None
	#pass one page html,return the "duanzi" list without picture
        def getPageItems(self,pageIndex):
	   pageCode=self.getPage(pageIndex)
	   if not pageCode:
 	      print "loading page failed....."
	      return None
  	   pattern=re.compile('<div class="author clearfix">.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>',re.S)
	   items=re.findall(pattern,pageCode)
            #to store every page of " duanzi"
           pageStories=[]
  	    #search all the useful information
   	   for item in items:
                replaceBR=re.compile('<br/>')
                text=re.sub(replaceBR,"\n",item[1])
                #item[0] is Author,item[1] is Content,item[2] is Favorite,item[3] is Comments
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
	   return pageStories
	#load and crawl the page content and add to the list
	def loadPage(self):
	     #if unseen page is less than 2 page then load the new page
	     if self.enable==True:
		if len(self.stories)<2:
		    #load new page
                    pageStories=self.getPageItems(self.pageIndex)
                    #put the page "duanzi" into global list
                    if pageStories:
                         self.stories.append(pageStories)
                         #pageIndex increasement to get the next page
                         self.pageIndex+=1
	#launch the method,when  command "Enter" to print a "duanzi"
        def getOneStory(self,pageStories,page):
              #search "duanzi" in one page
              for story in pageStories:
                  #wait the user to input
                  input=raw_input()
                  #when input to judge if loading new page
                  self.loadPage()
                  #if input quit ,the crawl is terminated
                  if input=="quit":
                       self.enable=False
                       return
                  print u"in %d page\t\nAuthor:%s\t\nContent:%s\t\nFavorite:%s\t\nComments:%s\n"%(page,story[0],story[1],story[2],story[3])
	#Start
	def start(self):
	     print "Reading the www.qiushibaike.com,input 'Enter' to get new 'duanzi',and use 'quit' to exit"
	     #set true to run the crawl
             self.enable=True
             #load one page
             self.loadPage()
             #local variable value to control read how many page
             nowPage=0
             while self.enable:
		if len(self.stories)>0:
                    #get one page "duanzi" from global list
                    pageStories=self.stories[0]
                    #incresement the readed page
                    nowPage+=1
                    #delete the item in global list for having read 
                    del self.stories[0]
                    #print the "duanzi" in the page
                    self.getOneStory(pageStories,nowPage)

spider=QSBK()
spider.start()
