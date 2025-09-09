import sys
import re
import logging
import gensim
import preprocess
from gensim import models
from gensim.models import LsiModel

from io import StringIO
from collections import Counter

class FileSource :
    def __init__(self,filename) :
        self.fp = open(filename,'r')

    def __iter__(self) :
        for line in self.fp :
            line = preprocess.SeparateFullStop(line)
            SB = StringIO() 
            preprocess.ReplaceUnicode(SB,line)
            line = SB.getvalue()
            line = line.lower()
            line = preprocess.DropChars(line, [ '^', '[', ']', '(', ')', '\'', '"', '-', ',', ';'] )
            yield line.split()




class MyCorpus :
    def __init__(self, trainfile) :
        self.fs = FileSource(trainfile)
        self.dictionary = gensim.corpora.Dictionary(self.fs)

    def BOW(self,filename) :
        bows = []
        fsrc = FileSource(filename)
        for line in fsrc :
            bows.append(self.dictionary.doc2bow(line))
        return bows

    def TOKEN(self,id) :
        return self.dictionary[id]

    def DICTIONARY(self) :
        return self.dictionary
    




if __name__ == '__main__' :
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO) 

    FS = FileSource('rfc793.txt')
    MC = MyCorpus('rfc793.txt')
    bows = MC.BOW('rfc793.txt')

    tfidf = models.TfidfModel(bows) 
    tfidf_corpus = tfidf[bows]

    #lsimodel = LsiModel(bows[:100], id2word=MC.DICTIONARY(), num_topics=8)
    #vectors = lsimodel[bows[150:155]]
    lsimodel = LsiModel(tfidf_corpus[:100], id2word=MC.DICTIONARY(), num_topics=8)
    vectors = lsimodel[tfidf_corpus[150:155]]
    topics = lsimodel.print_topics(8)
    #print(topics)


    for line in FS :
        print(line)
    print('\n\n')

    dict = MC.DICTIONARY()
    print(dict.token2id) 
    print('\n\n')
    print(dict.dfs) 
    print('\n\n')
    print(dict.cfs) 


    #print(vectors)
    #for v in vectors :
    #    print(v)
    #print('\n\n')

    #for ix in range(8) :
    #    lsimodel.show_topic(ix)
    #    print('---- --- ---- -- -- - - --- -------')


    #print(bows)
    #print('\n')
    #print(tfidf_corpus)
    #for doc in tfidf_corpus :
    #    print(doc)

    #for fs,bow in zip(FS,bows) :
    #    print(fs)
    #    for b in bow :
    #        print('({},{})'.format( MC.TOKEN(b[0]), b[1]),  end=' ')
    #    print('')


