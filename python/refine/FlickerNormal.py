
# coding: utf-8

# In[2]:

import sqlite3 as lite 
# from bidict import bidict

from math import *
# In[3]:

def NFD(ftij,fti,ftj,G = 2600000):
    fti = log(fti)
    ftj = log(ftj)
    ftij = log(ftij)
    return (max(fti,ftj) - ftij)/(log(G) - min(fti,ftj))

con = lite.connect('G:\\ImageAnnotation\\python\\yfcc10m.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()

flog = open('error.log','a')
startNum = 1
wordCount = 0
pageSize = 10000
i = 0
while True:
    if i % 10 == 0:
        print(i )
    if i == 100:
        break
    sql = 'SELECT e2.w1_id,counts.rowid as w2_id,e2.weight,e2.w1_weight,counts.weight as w2_weight FROM (SELECT counts.rowid as w1_id,e.word2,e.weight,counts.weight as w1_weight FROM (SELECT * FROM edges LIMIT %d OFFSET %d) e LEFT JOIN counts ON e.word1 = counts.word)e2 LEFT JOIN counts ON e2.word2=counts.word'%(pageSize,i * pageSize)
#     print(sql)
    cur.execute(sql)
    dbrows = cur.fetchall()

    tmpRowNum = 1
    for j in range(len(dbrows)):
        if dbrows[j][2] > 0:
            # row[ i * pageSize + j] = wordEntry[dbrows[j][0]]
            # col[ i * pageSize + j] = wordEntry[dbrows[j][1]]
            # data[i * pageSize + j] = NFD(dbrows[j][2],dbrows[j][3],dbrows[j][4])
            nowRowNum = i * pageSize + tmpRowNum
            if nowRowNum >= startNum:
                try:
                    cur.execute("INSERT INTO distance(word1, word2, distance) VALUES (?,?,?)",(dbrows[j][0],dbrows[j][1],NFD(dbrows[j][2],dbrows[j][3],dbrows[j][4])))
                except:
                    flog.write(str(dbrows[j][0])+ ' '+str(dbrows[j][1])+' '+str(NFD(dbrows[j][2],dbrows[j][3],dbrows[j][4]))+'\n')
        tmpRowNum += 1
    con.commit()
    if len(dbrows) < pageSize:
        break
    i += 1
print(str(wordCount))


