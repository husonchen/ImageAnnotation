import sqlite3 as lite
from ArangoSearch import ArangoSearcher

'''
Thing : is exact things
Concept : is abstract of Thing.
Category = Concept
Thing has no super class relationships. Only Concept has super class or sub class.
'''

class DbpediaQuery :
    searcher = []
    con = []
    def __init__(self):
        self.searcher = ArangoSearcher()
        # self.con = lite.connect('resource-concept.db')
        self.con = lite.connect('resource.db')
        self.con.text_factory = lambda x: unicode(x, "utf-8", "ignore")

    '''
    find all the concepts of a thing
    '''
    def getConceptsOfThing(self,thing) :
        thing = thing.lower()
        cur = self.con.cursor()
        cur.execute("SELECT * FROM subject WHERE resource='%s'" %thing)
        rows = cur.fetchall()
        concepts = []
        for row in rows:
            concepts.append(row[1])

        return concepts

    '''
    find the super class of a thing or class
    if input is a thing, firstly find the concept, then finding the super class
    As thing has more than 1 concepts, here I use only the first as the concept.
    '''
    def getSuperClass(self,tag,depth = 1):
        # if tag is not a concept, first find the concept
        concepts = self.getConceptsOfThing(tag)
        if len(concepts) != 0 :
            tag = concepts[0] #need further discuss
            #cost 1 depth to find the concept
            depth -= 1
        return self.searcher.searchBroaderCategory(tag, depth)



    '''
    find the smallest distance between two things or concept
    '''
    def getSmallestDistance(self,tag1,tag2):

        head = []
        tail = []
        concepts1 = self.getConceptsOfThing(tag1)
        if len(concepts1) != 0 :
            head = [[tag1.lower()]]
        else :
            return False

        concepts2 = self.getConceptsOfThing(tag2)
        if len(concepts2) != 0 :
            tail = [[tag2.lower()]]
        else :
            return False

        shortestPath = []
        shortlength = 65535
        for i in concepts1:
            path = self.searcher.shortestPathBetweenCategores(i,concepts2[0])
            if len(path) < shortlength:
                shortlength = len(path)
                shortestPath = path
                shortestStart = concepts1[i]

        for i in concepts2:
            path = self.searcher.shortestPathBetweenCategores(shortestStart,i)
            if len(path) < shortlength:
                shortlength = len(path)
                shortestPath = path
                shortestStart = concepts2[i]

        if len(shortestPath) == 0:
            return False
        return  head + shortestPath + tail

if __name__ == '__main__':
    query = DbpediaQuery()
    print "concept of Blue : " + str(query.getConceptsOfThing("Blue"))
    print "SuperClass 1 of blue : " + str(query.getSuperClass("blue"))
    print "SuperClass 2 of blue : " + str(query.getSuperClass("blue",2))
    print "SuperClass 1 of color : " + str(query.getSuperClass("color"))
    import time
    start = time.time() * 1000
    print "SmallestDistance between water and lake " + str(query.getSmallestDistance("water","lake"))
    end = time.time() * 1000
    print "cost time "+ str(end - start)