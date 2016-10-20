import requests

def getConceptOfThing(thing) :
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

def get
if __name__ == '__main__':
    getConceptOfThing("blue")