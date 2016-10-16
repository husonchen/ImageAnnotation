import numpy

if __name__ == '__main__':
    pairsMat = numpy.array([('','',0)],dtype = [('wikiUrl', 'S100'), ('name', 'S20'), ('count', int)])
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
                if count >= 4000:
                    pairsMat = numpy.append(pairsMat,numpy.array([(wikiUrl,name,count)],dtype = pairsMat.dtype))

    print i
    pairsMat[::-1].sort(order= 'count')
    f.close()
    f = open('test.txt', 'w')
    for sublist in pairsMat:
        for item in sublist:
            f.write(str(item)+'\t')
        f.write('\n')
    f.close()


