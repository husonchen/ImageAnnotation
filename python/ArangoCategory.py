from pyArango.connection import *

conn = Connection(username="root", password="imageannotation")

db = conn['_system']
usersCollection = db['category']


f = open('G:\\skos_categories_en.ttl\\skos_categories_en.ttl')
i = 0
start = 0
count = 0
data = []
for line in f:
    item = line.split(' ')
    if len(item) >= 3 and item[1] == '<http://www.w3.org/2004/02/skos/core#broader>' :

        count += 1
        if count <= start :
            continue
        if count % 100000 == 0:
            print count
        cat = item[0][1:-1].split(':')[-1]
        broadercat = item[2][1:-1].split(':')[-1]
        # data.append([cat,broadercat])
        doc = usersCollection.createDocument()
        doc._key = cat
        try:
            doc.save()
        except :
            pass

        doc = usersCollection.createDocument()
        doc._key = broadercat
        try :
            doc.save
        except :
            pass
