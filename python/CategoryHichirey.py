from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "imageannotation"))
session = driver.session()

# Insert data
insert_query = '''
UNWIND {pairs} as pair
MERGE (p1:class {name:pair[0]})
MERGE (p2:class {name:pair[1]})
'''

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
        i += 1
        cat = item[0][1:-1].split(':')[-1]
        broadercat = item[2][1:-1].split(':')[-1]
        data.append([cat,broadercat])
        if i == 1000 :
            session.run(insert_query, parameters={"pairs": data})
            i = 0
            data = []

session.run(insert_query, parameters={"pairs": data})
print count


#
# data = [["Jim","Mike"],["Jim","Billy"],["Anna","Jim"],
#           ["Anna","Mike"],["Sally","Anna"],["Joe","Sally"],
#           ["Joe","Bob"],["Bob","Sally"]]
#
# session.run(insert_query, parameters={"pairs": data})
#
# # Friends of a friend
#
# foaf_query = '''
# MATCH (person:Person)-[:KNOWS]-(friend)-[:KNOWS]-(foaf)
# WHERE person.name = {name}
#   AND NOT (person)-[:KNOWS]-(foaf)
# RETURN foaf.name AS name
# '''
#
# results = session.run(foaf_query, parameters={"name": "Joe"})
# for record in results:
#     print(record["name"])
#
#
# # Common friends
#
# common_friends_query = """
# MATCH (user:Person)-[:KNOWS]-(friend)-[:KNOWS]-(foaf:Person)
# WHERE user.name = {user} AND foaf.name = {foaf}
# RETURN friend.name AS friend
# """
#
# results = session.run(common_friends_query, parameters={"user": "Joe", "foaf": "Sally"})
# for record in results:
#     print(record["friend"])
#
# # Connecting paths
#
# connecting_paths_query = """
# MATCH path = shortestPath((p1:Person)-[:KNOWS*..6]-(p2:Person))
# WHERE p1.name = {name1} AND p2.name = {name2}
# RETURN path
# """
#
# results = session.run(connecting_paths_query, parameters={"name1": "Joe", "name2": "Billy"})
# for record in results:
#     print (record["path"])
#
#
# session.close()