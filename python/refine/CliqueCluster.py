

import sqlite3 as lite
import networkx as nx
# In[3]:

con = lite.connect('../yfcc100m.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()

flog = open('error.log','a')
startNum = 1
wordCount = 0
pageSize = 10000
i = 0
G = nx.Graph()
while True:
    if i % 10 == 0:
        print(i )
    if i == 100:
        break
    sql = 'select word1,word2,distance from distance where distance <  0.0001 LIMIT %d OFFSET %d'%(pageSize,i * pageSize)
#     print(sql)
    cur.execute(sql)
    dbrows = cur.fetchall()

    tmpRowNum = 1
    for j in range(len(dbrows)):
        if dbrows[j][2] > 0:
            G.add_node(dbrows[j][0])
            G.add_node(dbrows[j][1])
            G.add_edge(dbrows[j][0], dbrows[j][1])

    if len(dbrows) < pageSize:
        break
    i += 1

# In[6]:
cliques = nx.find_cliques(G)
f = open('clique_0.0001.data', 'w')
for i in cliques:
    if len(i) >= 4:
        placeholder = '?'  # For SQLite. See DBAPI paramstyle.
        placeholders = ', '.join(placeholder * len(i))
        sql = 'select word from counts where rowid in (%s)' % placeholders
        cur.execute(sql, i)
        rows = cur.fetchall()
        for row in rows:
            f.write(str(row[0]) + ' ')
        f.write('\n')
        f.flush()
        G.remove_nodes_from(i)
f.close()