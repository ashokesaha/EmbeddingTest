from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities

import sys
import os 




documents = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey",
]

doc = "Human computer interaction"




documents = []
FileSources = ['Food/biriyani.txt', 'Food/burrito.txt', 'Food/butter_chicken.txt',
               'Food/cake.txt', 'Food/chowmein.txt', 'Food/dosa.txt', 'Food/lasagne.txt' ]
Folders = ['Food','Biology','Festivals']

FileSAOURCES = []
for F in Folders :
    dirlist = os.listdir(F)
    filelist = [F+'/'+f for f in dirlist if os.path.isfile(F+'/'+f) if f.endswith('.txt')]  

    for filename in filelist :
        with open(filename,'r') as fp :
            FileSources.append(filename)
            documents.append(fp.read()) 

 
print('FileSources ::')
print(FileSources)
print()

#for ix, filename in enumerate(FileSources) :
#    with open(filename,'r') as fp :
#        documents.append(fp.read()) 


doc = 'spicy india chicken dish'
doc = 'dish with egg'
doc = 'baked dish  with batter and egg'



stoplist = set('for a of the and to in'.split())
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
corpus = tfidf[corpus]

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=4)
index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it

print('Ready ::')
for doc in sys.stdin :
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space

    sims = index[vec_lsi]  # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    print('Query: {}'.format(doc))
    for doc_position, doc_score in sims:
        print('{0:<32}    {1}'.format(FileSources[doc_position], doc_score))
        #print(doc_position, doc_score, documents[doc_position])

    print('\n')

