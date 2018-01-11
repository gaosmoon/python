# -*- coding:utf-8 -*-

__author__ = 'GS'

import urllib
import urllib2
import re
import thread
import time
import sys

# 创建一个糗事百科的类
class QSBK:
    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent' : self.user_agent}
        self.read_enable = 1
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []

    def SetPage(self, page):
            self.page_index = page;
    
    def GetPage(self, page):
            try:
                url = 'http://www.qiushibaike.com/hot/page/' + str(page)
                # 构建请求的request
                request = urllib2.Request(url, headers = self.headers)
                # 利用urlopen获取页面代码
                response = urllib2.urlopen(request)
                # 将页面转换为UTF-8编码
                page_content = response.read().decode('utf-8')
                return page_content
            except urllib2.URLError as e:
                if hasattr(e,"reason"):
                    print "连接糗事百科失败,错误原因", e.reason

    def GetData(self, page):
            content = self.GetPage(page)
            if not content:
                print '页面加载失败'
                return None
            pattern = re.compile(r'<div.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>', re.S)
            items = pattern.findall(content)
            # 用来存储每页的段子们
            page_stories = []
            # 遍历正则表达式匹配的信息
            for item in items:
                page_stories.append([item[0].strip(), item[1].strip()])
            
            return page_stories

    def LoadPage(self):
            # 如果当前未看的页数少于2页，则加载新一页 
            if self.read_enable == True:
                if len(self.stories) < 2:
                    # 获取新一页
                    page_stories = self.GetData(self.page_index)
                    # 将该页的段子存放到全局list中
                    if page_stories:
                        self.stories.append(page_stories)
                        # 获取完之后页码索引加一，表示下次读取下一页
                        self.page_index += 1
                        
            print "%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name)

    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.LoadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.read_enable = False
                return
            print u'第%d页\t发布人:%s\t\n%s' % (page, story[0], story[1])

    def Start(self):
        print '正在读取糗事百科，按回车查看新文章...'
        # 先加载一页内容
        self.LoadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.read_enable:
            if len(self.stories)>0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories,nowPage)

q = QSBK()
q.Start()

