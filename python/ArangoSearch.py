from pyArango.connection import *

class ArangoSearcher :

    conn = []
    db = []
    usersCollection = []
    edgeCollection = []
    my_graph = []

    def __init__(self):
        self.conn = Connection(arangoURL = 'http://husonchen.com:8529',username="root", password="imageannotation")
        self.db = self.conn['_system']
        self.usersCollection = self.db['category']
        self.edgeCollection = self.db['broader']
        self.my_graph = self.db.graphs['Koya']

    # def judgeIsCategory(self,category):
    #     category = category.capitalize()
    #     aql = "FOR doc IN category FILTER doc._key == '%s' RETURN doc" %category
    #     queryResult = self.db.AQLQuery(aql, rawResults=True, batchSize=100)
    #     if len(queryResult) > 0:
    #         return True
    #     return False

    def searchBroaderCategory(self,category,depth=1):
        category = category.lower()
        aql = "FOR v IN %s..%s OUTBOUND 'category/%s' GRAPH 'Koya' return DISTINCT(v._key)" % (depth ,depth ,category)
        queryResult = self.db.AQLQuery(aql, rawResults=True, batchSize=100)
        return queryResult

    def shortestPathBetweenCategores(self,category1,category2):
        category1 = category1.lower()
        category2 = category2.lower()
        aql = "FOR v, e IN ANY SHORTEST_PATH 'category/%s' TO 'category/%s' GRAPH 'Koya' RETURN [v._key]" % (category1 ,category2)
        queryResult = self.db.AQLQuery(aql, rawResults=True, batchSize=100)
        return queryResult.response['result']

    def shortestPathBetweenMultiCategores(self,categories1,categories2):
        start = ['category/'+cat.lower().encode('utf-8') for cat in categories1]
        end = ['category/'+cat.lower().encode('utf-8') for cat in categories2]
        aql = "FOR a IN %s FOR d IN %s " \
              "let path = (FOR v, e IN ANY SHORTEST_PATH a TO d GRAPH 'Koya' RETURN [v._key])" \
              "SORT LENGTH(path) ASC limit 1" \
              "return path" %(str(start),str(end))
        queryResult = self.db.AQLQuery(aql, rawResults=True, batchSize=100)
        return queryResult.response['result']

if __name__ == '__main__':
    searcher = ArangoSearcher()
    # print "Blue is category? : " + str(searcher.judgeIsCategory("Blue"))
    # print "Color is category? : " + str(searcher.judgeIsCategory("Color"))
    print "Color broader 2 categores : " + str(searcher.searchBroaderCategory("Color",2))
    print "Color to television : " + str(searcher.shortestPathBetweenCategores("Color","Television"))