import sys
import os
import re
import unicodedata

from io import StringIO
from collections import Counter


STOPWORDS = ['a', 'an', 'the', 'to', 'on', 'of', 'at', 'is', 'was', 'or', 'but', 'if', 'in', 'and', 'are', 'be', 'let', 'as']

def ReplaceUnicode(SB, line) :
    mystr = None
    for C in line :
        ucode = ord(C)

        if ucode == 0xbd :
            mystr = ' onehalf'
        elif ucode == 0xbc :
            mystr = ' onefourth'
        elif ucode == 0xbe :
            mystr = ' threefourth'
        elif ucode == 0x2150 :
            mystr = ' oneseventh'
        elif ucode == 0x2151 :
            mystr = ' onenineth'
        elif ucode == 0x2152 :
            mystr = ' onetenth'
        elif ucode == 0x2153 :
            mystr = ' onethird'
        elif ucode == 0x2154 :
            mystr = ' twothird'
        elif ucode == 0x2155 :
            mystr = ' onefifth'
        elif ucode == 0x2156 :
            mystr = ' twofifth'
        elif ucode == 0x2157 :
            mystr = ' threefifth'
        elif ucode == 0x2158 :
            mystr = ' fourfifth'
        elif ucode == 0x2159 :
            mystr = ' onesixth'
        elif ucode == 0x215a :
            mystr = ' fivesixth'
        elif ucode == 0x215b :
            mystr = ' oneeigth'
        elif ucode == 0x215c :
            mystr = ' threeeighth'
        elif ucode == 0x215d :
            mystr = ' fiveeighth'
        elif ucode == 0x215e :
            mystr = ' seveneighth'
        elif ucode > 127 :
            if ucode != 0xb0 :
                mystr = ' '
            else :
                mystr = str(C)
        else :
            mystr = str(C)

        SB.write(mystr)



def DropChars(line, droplist) :
    SB = StringIO()
    for C in line  :
        if C in droplist :
            SB.write(' ')
        else : 
            SB.write(C)

    line = SB.getvalue()
    return line



def SpoonHandle(line) :
    pattern = r"(tbsp\.*|tsp\.*|tablespoons*|teaspoons*)"
    line = re.sub(pattern, 'tsp', line)
    return line


def TemparatureHandler(line) :
    pattern = r"(\d+°[f|c])"
    line = re.sub(pattern, 'TMP', line)
    return line



def NUMPattern(W) :
    pat = re.compile('\d+$')
    if pat.match(W) :
        return 'NUM'
    return W

 

def TEMPPattern(W) :
    pat = re.compile('\d+°[c|f]$')
    if pat.match(W) :
        return 'TEMP'
    return W




def NumberHandler(line) :
    pattern = r"(\d+)"
    line = re.sub(pattern, 'NUM', line)

    pattern = r"\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|twenty|thirty|hundred)\s+"
    line = re.sub(pattern, ' NUM ', line)

    pattern = r"(NUMxNUM)"
    line = re.sub(pattern, 'NUM by NUM', line)

    pattern = r"(NUMg)"
    line = re.sub(pattern, 'NUM grams', line)

    pattern = r"(NUM\s+NUM)"
    line = re.sub(pattern, 'NUM', line)

    pattern = r"(NUM[-|\|\/|\.]NUM)"
    line = re.sub(pattern, 'NUM', line)

    pattern = r"(onehalf|onefourth|threefourth|oneseventh|onenineth|onetenth|onethird|twothird|onefifth|twofifth|threefifth|fourfifth|onesixth|fivesixth|oneeigth|threeeighth|fiveeighth|seveneighth)"
    line = re.sub(pattern, 'FRAC', line)

    return line



def SeparateFullStop(line) :
    pattern = r"([a-z])(\.)(\s+([A-Z]|$))"
    line = re.sub(pattern, r"\1 ^ \3", line)
    return line



if __name__ == '__main__' :
    with open('Food/small.csv','r') as f :
        all_sentences = []
        C = Counter()

        for line in f :
            line = SeparateFullStop(line)

            SB = StringIO() 
            ReplaceUnicode(SB,line)
            xstr = SB.getvalue()


            xstr = DropChars(xstr, [ '[', ']', '(', ')', '\'', '"', '-', ',', ';'] )
            xstr = xstr.lower()

            xstr = SpoonHandle(xstr)
            xstr = TemparatureHandler(xstr)
            xstr = NumberHandler(xstr)

            sent = xstr.split()
            sent.append('EOS')
            C.update(sent)
            all_sentences.append(sent)

        #print('\n\n')
        #print(C)

        for sent in all_sentences :
            print(sent)
        print('Total sentences {}'.format(len(all_sentences)))


