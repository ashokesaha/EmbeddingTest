import re
#import nltk
import sys

from gensim.test.utils import datapath
from gensim.models.word2vec import Text8Corpus
from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
from gensim.models import Word2Vec


def isNumber(W) :
    pattern = r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty|1eight|1four|1six|1two|3two|a|half|twothird|onefourth|threefourth|oneeighth|onefourth|onehalf|onethird|quarter|UNKFRAC)'

    P = re.compile(pattern)
    if P.match(W):
        return True
    else :
        return False


text = "Please give me a one glass of water and 3-lb of bread"
pattern = r"(\s|-)?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|\d+)(\s|-)?"



def xto_unicode(text, encoding='utf8', errors='strict'):
    if isinstance(text, str):
        return text
    return str(text, encoding, errors=errors)






class xText8Corpus:
    def __init__(self, fname, max_sentence_length=1024):
        self.fname = fname
        self.max_sentence_length = max_sentence_length

    def __iter__(self):
        sentence, rest = [], b''
        with open(self.fname, 'rb') as fin:
            while True:
                text = rest + fin.read(8192)  # avoid loading the entire file (=1 line) into RAM
                if text == rest:  # EOF
                    words = to_unicode(text).split()
                    sentence.extend(words)  # return the last chunk of words, too (may be shorter/longer)
                    if sentence:
                        yield sentence
                    break
                last_token = text.rfind(b' ')  # last token may have been split in two... keep for next iteration
                words, rest = (to_unicode(text[:last_token]).split(),
                               text[last_token:].strip()) if last_token >= 0 else ([], text)
                sentence.extend(words)
                while len(sentence) >= self.max_sentence_length:
                    yield sentence[:self.max_sentence_length]
                    sentence = sentence[self.max_sentence_length:]



if __name__ == '__main__' :
    #nltk.download('punkt')
    #nltk.download('stopwords')
    #with open('Food/small.csv','r') as f :
    #    D = f.read()
    #    S = nltk.tokenize.sent_tokenize(D)
    #    for s in S :
    #        print(s)
    #    print('\n\n')


    #T8 = Text8Corpus('Food/small.csv', max_sentence_length=128)
    #for s in T8 :
    #    print(s)
    #    print('')

    sentences = []
    with open('outt','r') as f :
        for line in f :
            sentences.append(line.split())

    w2v_model = Word2Vec(min_count=2,
        window=3, vector_size=32, sample=6e-5, 
        alpha=0.001, min_alpha=0.0001,
        hs=0, negative=5, workers=2)

    w2v_model.build_vocab(sentences, progress_per=100)

    w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

    print(w2v_model.wv.index_to_key)

