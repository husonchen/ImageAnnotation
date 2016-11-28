import numpy as np

import scipy.sparse as sps
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import sqlite3 as lite
from bidict import bidict
import pickle
from math import *

con = lite.connect('G:\\ImageAnnotation\\python\\SNAPCoocFull.db')
con.text_factory = lambda x: str(x, "utf-8", "ignore")
cur = con.cursor()
CoolCount = 27587694
row = np.zeros(CoolCount)
col = np.zeros(CoolCount)
data = np.zeros(CoolCount)
# change string to int data
wordEntry = pickle.load(open("../IPython/wordEntry.data", "rb"))
wordCount = 0
pageSize = 10000
totalPhoto = 250000


def NFD(fti,ftj,ftij,G = 250000):
    fti = log(fti)
    fti = log(fti)
    ftij = log(ftij)
    return (max(fti,ftj) - ftij)/(log(G) - min(fti,ftj))

def getPhotoNum(tag):
    sql = 'select sum(occurrences) from edges where word1 = \'%s\' OR word2 = \'%s\'' % (tag, tag)
    # print(sql)
    cur.execute(sql)
    dbrows = cur.fetchall()
    return dbrows[0][0]

if __name__ == '__main__':
    for i in range(int(CoolCount / pageSize) + 1):
        if i % 10 == 0:
            print(i)
        sql = 'select * from edges limit %d OFFSET %d' % (pageSize, i * pageSize)
        #     print(sql)
        cur.execute(sql)
        dbrows = cur.fetchall()
        #     print(dbrows)

        for j in range(len(dbrows)):
            if dbrows[j][2] > 0:
                row[i * pageSize + j] = wordEntry[dbrows[j][0]]
                col[i * pageSize + j] = wordEntry[dbrows[j][1]]
                tag1Num = getPhotoNum(dbrows[j][0])
                tag2Num = getPhotoNum(dbrows[j][1])
                data[i * pageSize + j] = NFD(tag1Num,tag2Num,dbrows[j][2],totalPhoto)
        if len(dbrows) < pageSize:
            break
    print(str(wordCount))
