import xml.sax
import re
import sqlite3 as lite

class PageHandler(xml.sax.ContentHandler):
    startNum = 12
    countNum = 0
    comitCount = 1000
    flog = open("error.log", "a")

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
            try:
                if int(self.pageId) > self.startNum:
                    cur.execute("INSERT INTO article(page_id, title) VALUES (?,?)" ,(self.pageId,self.pageTitle))
                    if self.countNum == self.comitCount:
                        con.commit()
                        self.countNum = 0
                    else :
                        self.countNum += 1
            except :
                self.flog.write(self.pageId + '   '+ self.pageTitle + '\n')
                print(self.pageTitle)
            self.CurrentData
            self.pageId = 0
            self.mentions = []
            self.pageRedict = False
            self.pageTitle = ''

        if tag == 'mediawiki':
            con.commit()
            self.flog.close()

    def characters(self, content):
        if self.pageTitle == '' and self.CurrentData == 'title':
            self.pageTitle = content
        if self.pageId == 0 and self.CurrentData == 'id':
            self.pageId = content


con = lite.connect('WikiGraph.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()
pattern = re.compile(r'\[\[.*?]]')

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler)
parser.parse("F:\\迅雷下载\enwiki-latest-pages-articles1.xml-p000000010p000030302.xml")
