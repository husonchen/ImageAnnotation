import xml.sax
import re
import sqlite3 as lite

class PageHandler(xml.sax.ContentHandler):
    CurrentData = ""
    pageId = 0
    mentions = []
    pageRedict = False
    pageTitle = ''

    def __init__(self):
        self.CurrentData
        self.pageId = 0
        self.mentions = []
        self.pageRedict = False
        self.pageTitle = ''

    #start event
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'redirect':
            self.mentions.append([attributes['title'],self.pageTitle])
            self.pageRedict = True


    def endElement(self,tag):
        if tag == "page":
            print("page end")
            self.CurrentData
            self.pageId = 0
            self.mentions = []
            self.pageRedict = False
            self.pageTitle = ''


    def characters(self, content):
        if self.pageTitle == '' and self.CurrentData == 'title':
            self.pageTitle = content
        if self.pageId == 0 and self.CurrentData == 'id':
            self.pageId = content
        if self.pageRedict == False and self.CurrentData == 'text':
            matchList = pattern.findall(content)
            for match in matchList:
                link = match[2:-2]
                a = link.split('|')
                if len(a) == 1:
                    self.mentions .append([a[0],a[0]])
                else :
                    # media file is not include
                    mediaPos = a[0].find(':')
                    if mediaPos < 0:
                        self.mentions.append([a[0],a[1]])

con = lite.connect('G:\\ImageAnnotation\\python\\yfcc10m.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()
pattern = re.compile(r'\[\[.*?]]')

def findPageId(pageNode):
    pageNode.getElementsByTagName('id')
    pass

def findMention():
    pass

def findOutGoing():
    pass

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler, )
parser.parse("F:\\迅雷下载\enwiki-latest-pages-articles1.xml-p000000010p000030302.xml")
