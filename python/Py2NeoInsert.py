from py2neo import Graph
import py2neo

graph = Graph(password = "imageannotataion")
batch = py2neo.WriteBatch(graph)

batch.create(node(name="Alice"))
batch.create(node(name="Bob"))
batch.create(rel(0, "KNOWS", 1))

f = open('G:\\skos_categories_en.ttl\\skos_categories_en.ttl')
i = 0
count = 0
data = []
for line in f:
    item = line.split(' ')
    if len(item) >= 3 and item[1] == '<http://www.w3.org/2004/02/skos/core#broader>' :
        i += 1
        count += 1
        cat = item[0][1:-1].split(':')[-1]
        broadercat = item[2][1:-1].split(':')[-1]
        data.append([cat,broadercat])
        if i == 1000 :
            session.run(insert_query, parameters={"pairs": data})
            i = 0
            data = []
