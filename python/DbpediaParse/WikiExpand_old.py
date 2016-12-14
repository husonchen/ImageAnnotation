import sqlite3 as lite
import sys

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
result = sorted(relatedWiki,key = relatedWiki.__getitem__)
for i in range(20):
    t = result[- (i + 1)]
    print(t+'|'+str(relatedWiki[t]) + '|' + str(relatedWikiNote[t]))