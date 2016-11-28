import xml.sax
import re
import sqlite3 as lite
import traceback

def addMentions(mentions,target,word):
    if target not in mentions:
        mentions[target] = {}
    if word not in mentions[target]:
        mentions[target][word] = 0
    mentions[target][word] += 1

def findMentions(content):
    mentions = {}
    content = content.replace('\n','')
    matchList = pattern.findall(content)
    for match in matchList:
        link = match[2:-2]
        a = link.split('|')
        if len(a) == 1:
            addMentions(mentions, a[0], a[0])
        else:
            # media file is not include
            mediaPos = a[0].find(':')
            if mediaPos < 0:
                addMentions(mentions, a[0], a[1])
    return mentions

class PageHandler(xml.sax.ContentHandler):
    startNum = 0
    countNum = 0
    comitCount = 1000
    flog = open("error.log", "a")

    CurrentData = ""
    pageId = 0
    pageRedict = False
    pageTitle = ''
    pageContent= ''

    def __init__(self):
        self.CurrentData
        self.pageId = 0
        self.pageRedict = False
        self.pageTitle = ''
        self.pageContent = ''


    #start event
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'redirect':
            self.pageContent += '[['+attributes['title']+'|'+self.pageTitle+']]'
            self.pageRedict = True


    def endElement(self,tag):
        if tag == "page":
            try:
                if int(self.pageId) > self.startNum:
                    mentions = findMentions(self.pageContent)
                    for target in mentions:
                        for word in mentions[target]:
                            appearCount = mentions[target][word]
                            cur.execute("INSERT INTO mentions(page_id, out_page_id, mention,weight) SELECT ?,page_id,?,? FROM article WHERE title = ? limit 1",(int(self.pageId),word,appearCount,target))
                    con.commit()
                    # if self.countNum == self.comitCount:
                    #     con.commit()
                    #     self.countNum = 0
                    # else :
                    #     self.countNum += 1
            except :
                traceback.print_exc()
                self.flog.write(self.pageId + '   '+ self.pageTitle + '\n')
                print(self.pageTitle)
            self.CurrentData
            self.pageId = 0
            self.pageRedict = False
            self.pageTitle = ''
            self.pageContent = ''

        if tag == 'mediawiki':
            con.commit()
            self.flog.close()

    def characters(self, content):
        if self.pageTitle == '' and self.CurrentData == 'title':
            self.pageTitle = content
        if self.pageId == 0 and self.CurrentData == 'id':
            self.pageId = content
        if self.pageRedict == False and self.CurrentData == 'text':
            self.pageContent += content


con = lite.connect('WikiGraph.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()
pattern = re.compile(r'\[\[.*?]]')

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler( Handler)
parser.parse("enwiki-latest-pages-articles1.xml-p000000010p000030302.xml")
