import xml.dom.minidom
import re
import sqlite3


dom = xml.dom.minidom.parse("F:\\迅雷下载\enwiki-latest-pages-articles1.xml-p000000010p000030302.xml")


# In[31]:

pattern = re.compile(r'\[\[.*?]]')
con = sqlite3.connect('linkage.db')
cur = con.cursor()
root = dom.documentElement
pages = root.getElementsByTagName('page')
for page in pages:
    title = page.getElementsByTagName('title')[0].firstChild.data
    content = page.getElementsByTagName('text')[0].firstChild.data
    it = pattern.finditer(content)
    sql = 'insert into links(title,linked,mention) values '
    for match in it:

    




