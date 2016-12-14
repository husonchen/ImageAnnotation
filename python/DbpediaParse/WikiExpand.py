import sqlite3 as lite
import sys
from DbpediaQuery import *
from functools import cmp_to_key

dbquery = DbpediaQuery()
con = lite.connect('WikiGraph.db_bk')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()

queryWords = ''
for i in range(1,len(sys.argv) - 1):
    queryWords = queryWords+sys.argv[i]+' '
queryWords = queryWords + sys.argv[len(sys.argv) - 1]
queryWikis = queryWords.split('~')
print(queryWikis)
relatedWikiNote= {}
relatedWiki = {}
for i in range(len(queryWikis)):
    esaRankPoint = 1 /(i + 1)
    query = 'SELECT article.title,m.weight FROM ' \
            '(SELECT mentions.page_id, mentions.weight FROM mentions ' \
            'WHERE out_page_id =( SELECT page_id FROM article WHERE title = ?)' \
            ') m LEFT JOIN article ON article.page_id=m.page_id'
    cur.execute(query,[queryWikis[i]])
    rows = cur.fetchall()
    for row in rows:
        title = row[0]
        linkWeight = row[1]
        weight = esaRankPoint * linkWeight
        if title not in relatedWiki:
            relatedWiki[title] = weight
            relatedWikiNote[title] = [queryWikis[i]+'-'+title+'-'+str(weight)]
        else:
            relatedWiki[title] += weight
            relatedWikiNote[title] += [queryWikis[i] + '-' + title +'-'+ str(weight)]

result = sorted(relatedWiki,key = relatedWiki.__getitem__,reverse = True)
sameScoreList = []
for i in range(20):
    t = result[i]
    distance = 0
    for query in queryWikis:
        distance += dbquery.getSmallestDistance(query.replace(' ','_'),t.replace(' ','_'))
    if distance == 0:
        continue
    if len(sameScoreList) == 0 or len(sameScoreList[-1]) == 0 :
        sameScoreList += [{t:distance}]
    else:
        lastScoreDict = sameScoreList[-1]
        lastScore = relatedWiki[result[i -1]]
        if relatedWiki[t] == lastScore:
            lastScoreDict[t] = distance
        else :
            # add next set
            sameScoreList += [{t:distance}]

print(sameScoreList)
resultList = []
for sameScoreSet in sameScoreList:
    result = sorted(sameScoreSet,key = sameScoreSet.__getitem__)
    for r in result:
        print(r+'|'+str(relatedWiki[r]) + '|' + str(relatedWikiNote[r])+'|'+str(sameScoreSet[r]))