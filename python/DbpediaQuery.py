import requests
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
    find all the concepts of a thing
    '''
    def getConceptsOfThing(self,thing) :
        thing = thing.capitalize()
        url = "http://dbpedia.org/sparql"
        query = {
            'query' : 'SELECT ?a WHERE {<http://dbpedia.org/resource/%s> dct:subject ?a}' % thing,
            "default-graph-uri" : "http://dbpedia.org",
            "format" : "text/csv"
            }

        headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
        r = requests.get(url , params=query ,headers = headers)

        results = r._content.split('\n')[1:-1]
        concepts = []
        for result in results :
            concepts .append(result[1:-1].split(":")[-1])

        return concepts

    '''
    find the super class of a thing or class
    if input is a thing, firstly find the concept, then finding the super class
    As thing has more than 1 concepts, here I use only the first as the concept.
    '''
    def getSuperClass(self,tag,depth = 1):
        # if tag is not a concept, first find the concept
        if self.searcher.judgeIsCategory(tag) == False :
            tags = self.getConceptsOfThing(tag)
            if len(tags) == 0:
                # different find concept
                return False
            else :
                tag = tags[0] #need further discuss
                #cost 1 depth to find the concept
                depth -= 1

        if depth > 0 :
            return self.searcher.searchBroaderCategory(tag,depth)
        return [tag]

    '''
    find the smallest distance between two things or concept
    '''
    def getSmallestDistanceWithOnlyConcept(self,tag1,tag2):
        # if tag is not a concept, first find the concept
        if self.searcher.judgeIsCategory(tag1) == False :
            tags = self.getConceptsOfThing(tag1)
            if len(tags) == 0:
                # different find concept
                return False
            else:
                tag1 = tags[0]  # need further discuss

        if self.searcher.judgeIsCategory(tag2) == False:
            tags = self.getConceptsOfThing(tag2)
            if len(tags) == 0:
                # different find concept
                return False
            else:
                tag2 = tags[0]  # need further discuss

        return self.searcher.shortestPathBetweenCategores(tag1,tag2)

    '''
    find the smallest distance between two things or concept
    '''
    def getSmallestDistance(self,tag1,tag2):
        path = self.getSmallestDistanceWithOnlyConcept(tag1,tag2)
        if path == False:
            return False
        if path[0][0] != tag1 :
            path = [[tag1.capitalize()]] + path
        if path[-1][0] != tag2 :
            path.append([tag2.capitalize()])
        return path

if __name__ == '__main__':
    query = DbpediaQuery()
    print "concept of blue : " + str(query.getConceptsOfThing("blue"))
    print "SuperClass 1 of blue : " + str(query.getSuperClass("blue"))
    print "SuperClass 2 of blue : " + str(query.getSuperClass("blue",2))
    print "SuperClass 1 of color : " + str(query.getSuperClass("color"))
    print "SmallestDistance between blue and Airline " + str(query.getSmallestDistance("blue","Airline"))
