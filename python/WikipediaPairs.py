import numpy

if __name__ == '__main__':
    pairsMat = numpy.array([('','',0)],dtype = [('wikiUrl', 'S100'), ('name', 'S20'), ('count', int)])
    pairsMat1 = numpy.array([('','',0)],dtype = [('wikiUrl', 'S100'), ('name', 'S20'), ('count', int)])
    pairsMat2 = numpy.array([('','',0)],dtype = [('wikiUrl', 'S100'), ('name', 'S20'), ('count', int)])
    pairsMat3 = numpy.array([('','',0)],dtype = [('wikiUrl', 'S100'), ('name', 'S20'), ('count', int)])
    mat1Num = 0
    mat2Num = 0
    mat3Num = 0
    print "mat1Num:" + str(mat1Num) + " mat2Num:" + str(mat2Num) + " mat3Num:" + str(mat3Num)
    f = open('H:\\image annotation\\Dbpedia Spotlight\\en\\tokenCounts')

    i = 0
    for line in f:
        i += 1
        if i % 100000 == 0:
            print i
        # print line
        lines = line.split('\t')
        wikiUrl = lines[0]
        arounds = lines[1][2:-3]
        entities = arounds.split('),(')
        for entity in entities:
            # print entity
            if len(entity.split(',')) > 1:
                name = ''.join(entity.split(',')[0:-1])
                count = int(entity.split(',')[-1])
                count = int(entity.split(',')[-1])
                if count >= 4000:
                    pairsMat = numpy.append(pairsMat, numpy.array([(wikiUrl, name, count)], dtype=pairsMat.dtype))
                elif count >= 1000 and count < 2000:
                    mat1Num += 1;
                    if mat1Num < 2000:
                        pairsMat1 = numpy.append(pairsMat1,numpy.array([(wikiUrl,name,count)],dtype = pairsMat1.dtype))
                elif count >= 2000 and count < 3000 :
                    mat2Num += 1;
                    if mat2Num < 2000:
                        pairsMat2 = numpy.append(pairsMat2,numpy.array([(wikiUrl,name,count)],dtype = pairsMat2.dtype))
                elif count >= 3000 and count < 4000 :
                    mat3Num += 1;
                    if mat3Num < 2000:
                        pairsMat3 = numpy.append(pairsMat3,numpy.array([(wikiUrl,name,count)],dtype = pairsMat3.dtype))


    print "mat1Num:" + str(mat1Num) + " mat2Num:"+str(mat2Num) + " mat3Num:"+str(mat3Num)
    f.close()
    f = open('coourance-1000-2000(2000samples).txt', 'w')
    for sublist in pairsMat1:
        for item in sublist:
            f.write(str(item)+'\t')
        f.write('\n')
    f.close()
    f = open('coourance-2000-3000(2000samples).txt', 'w')
    for sublist in pairsMat2:
        for item in sublist:
            f.write(str(item)+'\t')
        f.write('\n')
    f.close()
    f = open('coourance-3000-4000(2000samples).txt', 'w')
    for sublist in pairsMat3:
        for item in sublist:
            f.write(str(item) + '\t')
        f.write('\n')
    f.close()

    print i
    pairsMat[::-1].sort(order='count')
    f.close()
    f = open('result.txt', 'w')
    for sublist in pairsMat:
        for item in sublist:
            f.write(str(item) + '\t')
        f.write('\n')
    f.close()

