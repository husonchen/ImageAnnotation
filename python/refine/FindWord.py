import pickle
import json

wordEntry = pickle.load(open("../IPython/wordEntry.data", "rb"))

f = open('clique.data')
out = open('clique_word','w')
for line in f:
    clique = json.loads(line)
    words = []
    for i in clique:
        words.append(wordEntry.inv[int(i)])
    try:
        out.write(str(words) + '\n')
    except :
        pass
out.close()