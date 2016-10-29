import sqlite3
from gexf import Gexf

con=[]

def findBSiblings(words):
    words = tuple(words)
    if len(words) == 1:
        sql = "SELECT * FROM category WHERE concept in %s" % str(words)[0:-2] + ")"
    else:
        sql = "SELECT * FROM category WHERE concept in %s" % str(words)

    cur = con.cursor()
    # print sql
    cur.execute(sql)
    rows = cur.fetchall()
    edges = []
    for row in rows:
        edges.append([row[0].encode('utf-8'),row[1].encode('utf-8')])

    return edges

if __name__ == '__main__':
    con = sqlite3.connect("../python/resource.db")
    con.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    cur = con.cursor()

    nodeSet = set()
    edgeSet = {}
    newNode = set(['color'])


    for i in range(3):
        edges = findBSiblings(newNode)
        currentSiblingSet = set()

        for edge in edges:
            currentSiblingSet.add(edge[0])
            currentSiblingSet.add(edge[1])
            if edgeSet.has_key(edge[0]+"_"+edge[1]) == False and edgeSet.has_key(edge[1]+"_"+edge[0]) == False:
                edgeSet[edge[0]+"_"+edge[1]] = edge

        newNode = currentSiblingSet - nodeSet
        nodeSet = nodeSet | newNode

    gexf = Gexf("Husonchen", "A hello world! file")
    graph = gexf.addGraph("undirected", "static", "categories")

    for node in nodeSet:
        graph.addNode(node, node)

    i = 0
    for edge in edgeSet.values():
        graph.addEdge(str(i),edge[0] , edge[1])
        i += 1

    output_file = open("helloworld.gexf", "w")
    gexf.write(output_file)