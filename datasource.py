import sys
import re
import logging
import gensim
import preprocess
from gensim import models
from gensim.models import LsiModel

from io import StringIO
from collections import Counter

from verbs import rootVerb


class FileSource :
    def __init__(self,filename) :
        self.filename = filename
        self.fp = open(filename,'r')

    def __iter__(self) :
        Lines = []

        for line in self.fp :
            line = preprocess.SeparateFullStop(line)
            SB = StringIO() 
            preprocess.ReplaceUnicode(SB,line)
            line = SB.getvalue()
            line = line.lower()
            line = preprocess.DropChars(line, [ '^', '[', ']', '(', ')', '\'', '"', '-', ',', ';'] )

            line = line.split()
            line = [l for l in line if l not in preprocess.STOPWORDS]
            line = [preprocess.NUMPattern(w) for w in line]
            line = [preprocess.TEMPPattern(w) for w in line]
            line = [rootVerb(w) for w in line]

            for W in line :
                Lines.append(W)
        yield Lines


    def rewind(self) :
        self.fp = open(self.filename,'r')






class MahaFileSource :
    def __init__(self,filenames) :
        self.fss = []
        for filename in filenames :
            self.fss.append(FileSource(filename))


    def rewind(self) :
        for fs in self.fss :
            fs.rewind()


    def __iter__(self) :
        for fs in self.fss :
            for line in fs :
                yield line






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





class MahaCorpus :
    def __init__(self, trainfiles) :
        self.trainfiles = trainfiles
        self.mfs = MahaFileSource(trainfiles)
        self.dictionary = gensim.corpora.Dictionary(self.mfs)
        self.corpus = None

    def BuildCorpus(self) :
        self.mfs.rewind()
        lines = [line for line in self.mfs]
        self.corpus = [self.dictionary.doc2bow(line) for line in lines]


    def TOKEN(self,id) :
        return self.dictionary[id]

    def DICTIONARY(self) :
        return self.dictionary
    
    def CORPUS(self) :
        return self.corpus

    def FILES(self) :
        return self.trainfiles




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



'''
import datasource as ds
MC = ds.MahaCorpus(['Food/cake.txt', 'Food/dosa.txt', 'Food/pizza.txt'])
MC.BuildCorpus()
D = MC.DICTIONARY()
D.token2id
D.cfs
D.dfs
C = MC.CORPUS()
model = TfidfModel(C)
'''
