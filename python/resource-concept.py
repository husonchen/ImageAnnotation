
fw = open('resource-concept.txt', 'w')
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
    if len(item) >= 3 and item[1] == '<http://purl.org/dc/terms/subject>' :
        cat = item[0][1:-1].split('/')[-1]
        broadercat = item[2][1:-1].split(':')[-1]
        fw.write(cat + '\t' + broadercat + '\n')

fw.close()
f.close()