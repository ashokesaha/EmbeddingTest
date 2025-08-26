import sys
import os
import re
import unicodedata
import pandas as pd

from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

from tokenizers import          Tokenizer
from tokenizers.models import   BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.models import   WordPiece
from tokenizers.trainers import WordPieceTrainer
from tokenizers.pre_tokenizers import Whitespace
import trainfiles
import ashoke_regex

def read_files_from_folders(folder_list):
    file_contents = []
    for folder in folder_list:
        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents.append(f.read().lower())
    return file_contents



def read_sentences_from_file_content(file_contents) :
    sentence_list = []
    for f in file_contents :
        sents = sent_tokenize(f)
        for s in sents :
            sentence_list.append(s)

    return sentence_list


def read_sentences_from_string(S) :
    sentence_list = []
    sents = sent_tokenize(S)
    for s in sents :
        sentence_list.append(s)

    return sentence_list






def nltk_tokenize_sentences(sentence_list) :
    stop_words = set(stopwords.words('english'))

    stop_words.add(',')
    stop_words.add('.')
    stop_words.add(':')
    stop_words.add('"')
    stop_words.add('!')
    stop_words.add('#')
    stop_words.add('$')
    stop_words.add('>')
    stop_words.add(';')
    stop_words.add(')')
    stop_words.add('(')

    word_list = []
    for s in sentence_list :
        wl = word_tokenize(s)
        wl = [w for w in wl if w not in stop_words]
        word_list.append(wl)

    return word_list


def bpe_tokenize_sentences(sentence_list) :
    word_list = []
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
    tokenizer.train(trainfiles.TrainFiles, trainer)

    for s in sentence_list :
        wl = tokenizer.encode(s)
        word_list.append(wl.tokens)

    return word_list



def wordpiece_tokenize_sentences(sentence_list) :
    word_list = []
    tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = WordPieceTrainer(vocab_size=30522, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
    tokenizer.train(trainfiles.TrainFiles, trainer)

    for s in sentence_list :
        wl = tokenizer.encode(s)
        word_list.append(wl.tokens)

    return word_list



def word_list_to_counter(WL) :
    C = None
    for wl in WL :
        if not C :
            C = Counter(wl)
        else :
            C.update(wl)

    return C



def unicode_to_str(ucodes) :
    ucode = ord(ucodes)

    if ucode == 0xbd :
        return ' onehalf'
    elif ucode == 0xbc :
        return ' onefourth'
    elif ucode == 0xbe :
        return ' threefourth'
    elif ucode == 0x2150 :
        return ' oneseventh'
    elif ucode == 0x2151 :
        return ' onenineth'
    elif ucode == 0x2152 :
        return ' onetenth'
    elif ucode == 0x2153 :
        return ' onethird'
    elif ucode == 0x2154 :
        return ' twothird'
    elif ucode == 0x2155 :
        return ' onefifth'
    elif ucode == 0x2156 :
        return ' twofifth'
    elif ucode == 0x2157 :
        return ' threefifth'
    elif ucode == 0x2158 :
        return ' fourfifth'
    elif ucode == 0x2159 :
        return ' onesixth'
    elif ucode == 0x215a :
        return ' fivesixth'
    elif ucode == 0x215b :
        return ' oneeigth'
    elif ucode == 0x215c :
        return ' threeeighth'
    elif ucode == 0x215d :
        return ' fiveeighth'
    elif ucode == 0x215e :
        return ' seveneighth'

    return str(ucodes)





def check_temp(W) :
    pat = re.compile(r'\d+?°f')
    if pat.match(W) :
        return 'TTEMPP' 
    return W 



def CheckUnicode (filename) :
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    non_ascii = [ch for ch in text if ord(ch) > 127]
    for na in non_ascii :
        print('{:#x}-{}'.format(ord(na),na), end=' ')






def PandasRead(filename) :
    df = pd.read_csv(filename)
    df = df.dropna()
    rowcount = df.shape[0]

    for ix in range(rowcount) :
        try :
            ing = df.loc[ix].at['Title']
            ing = ing.lower()
            df.at[ix,'Title'] = ing 
        except KeyError as e :
            continue
 
        ing = df.loc[ix].at['Ingredients']
        ing = ''.join(map(unicode_to_str,ing))
        ing = ing.lower()
        df.at[ix,'Ingredients'] = ing 

        ing = df.loc[ix].at['Instructions']
        ing = ''.join(map(unicode_to_str,ing))
        ing = ing.lower()
        df.at[ix,'Instructions'] = ing 

    return df





def PrintOneSentence(sent) :
    for W in sent.split() :
        print(W,end=' ')
    print('')




def PrintSentences(sent_list) :
    for sent in sent_list :
        PrintOneSentence(sent)
        #print('----------------------')




if __name__ == '__main__' :
    nltk.download('punkt')
    nltk.download('stopwords')
    pd.set_option('display.max_colwidth', None)

    df = PandasRead(r'Food/13k-recipes.csv')
    rowcount = df.shape[0]

    all_sentences = []
    sentence_list = []

    C = Counter()

    for ix in range(rowcount) :
        try :
            Title        = df.loc[ix].at['Title']
            Ingredients  = df.loc[ix].at['Ingredients']
            Instructions = df.loc[ix].at['Instructions']
        except KeyError as e :
            continue

        sentence_list.append('Here is the recipe for ' + Title + ' ' + 'EEOSS')

        ing = ashoke_regex.process_Ingredients(Ingredients)
        sentence_list.append('Here are the necessary ingredients')
        for s in ing :
            sentence_list.append(s + ' ' + 'EEOSS>')


        Instructions = ashoke_regex.process_Instructions(Instructions)
        sl = read_sentences_from_string(Instructions)
        for sent in sl :
            sentence_list.append(sent + ' ' + 'EEOSS')
            all_sentences.append(sent + ' ' + 'EEOSS')

        word_list = nltk_tokenize_sentences(sentence_list)

        for wl in word_list :
            C.update(wl)

        sentence_list = []
        #if ix >= 500 :
        #    break


    PrintSentences(all_sentences)

