from pyArango.connection import *
from requests.auth import HTTPBasicAuth
import requests

conn = Connection(arangoURL = 'http://husonchen.com:8529',username="root", password="imageannotation")

db = conn['_system']
usersCollection = db['category']
edgeCollection = db['broader']
db.graphs
my_graph = db.graphs['Koya']

f = open('G:\\skos_categories_en.ttl\\skos_categories_en.ttl')
i = 0
start = 0
count = 0
data = []
for line in f:
    count += 1
    if count <= start:
        continue
    if count % 100000 == 0:
        print count
    item = line.split(' ')
    if len(item) >= 3 and item[1] == '<http://www.w3.org/2004/02/skos/core#broader>' :
        cat = item[0][1:-1].split(':')[-1]
        broadercat = item[2][1:-1].split(':')[-1]

        url = "http://localhost:8529/_api/gharial/Koya/edge/broader"
        d = {
            "type": "broader",
            "_from": "category/" + cat,
            "_to": "category/" + broadercat
        }
        r = requests.post(url, data=json.dumps(d),auth=HTTPBasicAuth('root', 'imageannotation'))

        # print "traversal json:", r
