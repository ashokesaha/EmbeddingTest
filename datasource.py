import sys
import re
import gensim
import preprocess

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

    




if __name__ == '__main__' :
    #fs = FileSource('Food/small.csv')
    #dict = gensim.corpora.Dictionary(fs)
    #print('')
    #print(dict)
    #print(dict.token2id)
    #print('\n\n')
    #print(dict.cfs)
    #print('\n\n')
    #print(dict.dfs)


    MC = MyCorpus('Food/small.csv')
    bows = MC.BOW('bow.txt')
    for bow in bows :
        print(bow)
        for b in bow :
            print('({},{})'.format( MC.TOKEN(b[0]), b[1]),  end=' ')
        print('')


