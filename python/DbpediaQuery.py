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
        cur.execute("SELECT concept FROM subject WHERE resource='%s'" %thing)
        rows = cur.fetchall()
        concepts = []
        for row in rows :
            concepts.append(row[0].encode('utf-8'))
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
            tag = concepts
            depth -= 1
        return list(self.searchBroaderCategory(tag, depth))

    def searchBroaderCategory(self,concepts,depth):
        # if depth <= 0 :
        #     return concepts

        for i in range(depth):
            concepts = self.findBroaderCategories(concepts)
        return concepts

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

        pathLength = self.deepFirstSearch(concepts1,concepts2)

        if pathLength == False:
            return False
        return  pathLength + 2

    def deepFirstSearch(self,concepts1,concepts2):
        startSetList = [set(concepts1)] # start set,every element of this list is a set
        endSetList = [set(concepts2)]

        met = startSetList[0].intersection(endSetList[0])
        if len(met) != 0 :
            return 1
        # if(met)
        maxDepth = 6
        shortlength = 65535
        isFind = False
        for i in range(0,maxDepth):
            # find the entry of this depth
            broaderCategories = self.findBroaderCategories(startSetList[i])
            #compare to every categories in endSetList
            for j in range(len(endSetList)):
                inter = endSetList[j].intersection(broaderCategories)
                if len(inter) != 0 :
                    # arealdy find the path
                    shortlength = i + j + 2
                    isFind = True
                    break
            if isFind :
                break
            # not find the path, store it
            startSetList.append(broaderCategories)

            # next extend end concept
            broaderCategories = self.findBroaderCategories(endSetList[i])
            # compare to every categories in startSetList
            for j in range(len(endSetList)):
                inter = startSetList[j].intersection(broaderCategories)
                if len(inter) != 0:
                    # arealdy find the path
                    shortlength = i + j + 2
                    isFind = True
                    break
            if isFind :
                break
            endSetList.append(broaderCategories)

        if isFind :
            return shortlength
        else:
            return False


    def findBroaderCategories(self,concepts):
        concepts = tuple(concepts)
        cur = self.con.cursor()
        sql = "SELECT broader FROM category WHERE concept in %s" % str(concepts)
        print sql
        cur.execute(sql)
        rows = cur.fetchall()
        concepts = set()
        for row in rows:
            concepts.add(row[0].encode('utf-8'))

        return concepts


if __name__ == '__main__':
    query = DbpediaQuery()
    print "concept of Blue : " + str(query.getConceptsOfThing("Blue"))
    print "SuperClass 1 of blue : " + str(query.getSuperClass("blue"))
    print "SuperClass 2 of blue : " + str(query.getSuperClass("blue",2))
    print "SuperClass 1 of color : " + str(query.getSuperClass("color"))
    import time
    start = time.time() * 1000
    print "SmallestDistance between water and lake " + str(query.getSmallestDistance("blue","airline"))
    end = time.time() * 1000
    print "cost time "+ str(end - start)