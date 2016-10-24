import time
from ArangoSearch import ArangoSearcher

'''
Thing : is exact things
Concept : is abstract of Thing.
Category = Concept
Thing has no super class relationships. Only Concept has super class or sub class.
'''

class DbpediaQuery :
    searcher = []

    def __init__(self):
        self.searcher = ArangoSearcher()

    '''
    find the super class of a thing or class
    '''
    def getSuperClass(self,tag,depth = 1):

        if depth > 0 :
            return self.searcher.searchBroaderCategory(tag,depth)
        return [tag]

    '''
    find the smallest distance between two things or concept
    '''
    def getSmallestDistance(self,tag1,tag2):
        return self.searcher.shortestPathBetweenCategores(tag1, tag2)

if __name__ == '__main__':
    query = DbpediaQuery()
    start = time.time() * 1000
    print "SuperClass 1 higher level of blue : " + str(query.getSuperClass("blue"))
    print "SuperClass 2 higher level of blue : " + str(query.getSuperClass("blue",2))
    print "SuperClass 1 higher level of color : " + str(query.getSuperClass("color"))
    print "SmallestDistance between blue and Airline " + str(query.getSmallestDistance("blue","Airline"))
    end = time.time() * 1000
    print "Cost Time = "+str(end-start) +" ms"