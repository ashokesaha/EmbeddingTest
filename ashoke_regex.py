import re
import sys

def replace_fraction(match) :
    frac = match.group(0)

    if frac == '1/2' :
        return 'half'
    elif frac == '1/3' :
        return 'onethird'
    elif frac == '1/5' :
        return 'onetfifth'
    elif frac == '1/7' :
        return 'onetseventh'
    elif frac == '1/9' :
        return 'onenineth'
    elif frac == '1/10' :
        return 'onetenth'
    elif frac == '2/3' :
        return 'twothird'
    elif frac == '2/5' :
        return 'twofifth'
    elif frac == '3/5' :
        return 'threefifth'
    elif frac == '3/7' :
        return 'threeseventh'
    elif frac == '5/7' :
        return 'fiveseventh'
    elif frac == '1/4' :
        return 'quarter'
    elif frac == '3/4' :
        return 'threefourth'
    elif frac == '1/8' :
        return 'oneeighth'
    
    return 'UNKFRAC'




def isNumber(W) :
    pattern = r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty|1eight|1four|1six|1two|3two|a|half|twothird|onefourth|threefourth|oneeighth|onefourth|onehalf|onethird|quarter|UNKFRAC)'

    P = re.compile(pattern)
    if P.match(W):
        return True
    else :
        return False




def replace_volume(match):
    L = match.group().split()

    if not isNumber(L[-2]) :
        return ' '.join(L)
    if not isNumber(L[-3]) :
        return ' '.join([L[-3],'VVOLUMEE'])

    return 'VVOLUMEE'





def replace_square_brace(match) :
    S = match.group(0)
    match = None
    result = re.match(r'\[(.*?)\]', S)
    if result :
        result = result.group(1)
    if not result :
        result = '<UNKNOWN>'

    return result 



def replace_round_brace(match) :
    S = match.group(0)
    match = None
    result = re.match(r'\((.*?)\)', S)
    if result :
        result = result.group(1)
    if not result :
        result = '<UNKNOWN>'

    return result 



def replace_single_quote(match) :
    S = match.group(0)
    match = None
    result = re.match(r'\'(.*?)\'', S)
    if result :
        result = result.group(1)
    if not result :
        result = '<UNKNOWN>'

    return result 


def replace_linebreak(match) :
    return '  --  '


def replace_temp(match) :
    S = match.group(0)
    result = re.match(r'\d+?°[fc]*', S)
    if result :
        result = 'TTEMPP' 
    else :
        result = 'UNK'

    return result 


def replace_ttempp(match) :
    return 'TTEMPP'


def replace_time(match) :
    return 'TTIMEE'


def replace_tbsp(match) :
    return 'TTBSPP'


def replace_ounce(match) :
    return 'VVOLUMEE'

def replace_number(match) :
    return 'NNUMBERR'




PATMATCH = {}
FUNCMATCH = {}
KEYS = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp', 'time', 'volume', 'tbsp', 'ounce', 'ttempp']

PATMATCH['fraction'] = r'([1-9]+/[1-9]+)'
PATMATCH['square_brace'] = r'(\[.*?\])'
PATMATCH['single_quote'] = r'(\'.*?\')' 
PATMATCH['linebreak'] = r'(\'\s*,\s*\'?)' 
PATMATCH['temp']  =  '(\d+(-\d+)*)°[fc]'
PATMATCH['time']  =  r'(\d+(.\d+)* (minutes|days|hours|seconds))' 
PATMATCH['volume'] = r'(\w+)\s+(\w+) (drops*|pints*|cups*|liters*|glass|glasses)'
PATMATCH['tbsp']  =  r"(\d+\-\d+)|\w+\s+tbsp\.*"
PATMATCH['ttempp']  = r"(TTEMPP[/-])+(TTEMPP)*" 
PATMATCH['ounce']  = r"(\d+|half|quarters*)(-|\s+)(oz|ounces*|quarts*)"
PATMATCH['number']  = r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"


FUNCMATCH['fraction'] = replace_fraction 
FUNCMATCH['square_brace'] = replace_square_brace
FUNCMATCH['single_quote'] = replace_single_quote 
FUNCMATCH['linebreak'] = replace_linebreak 
FUNCMATCH['temp'] = replace_temp 
FUNCMATCH['ttempp'] = replace_ttempp 
FUNCMATCH['time'] = replace_time 
FUNCMATCH['volume'] = replace_volume 
FUNCMATCH['tbsp'] = replace_tbsp 
FUNCMATCH['ounce'] = replace_ounce 
FUNCMATCH['number'] = replace_number 



def process_Ingredients(S) :
    #IK = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp', 'time', 'volume', 'tbsp', 'ounce', 'number']
    IK = []
    for K in IK :
        S = re.sub(PATMATCH[K], FUNCMATCH[K], S)

    return S
    #return S.split('  --  ')



def process_Instructions(S) :
    #IK = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp', 'time', 'volume', 'tbsp', 'ounce', 'number']
    IK = []
    for K in IK :
        S = re.sub(PATMATCH[K], FUNCMATCH[K], S)

    return S
    #return S.split('  --  ')



def replace_nmbr(match) :
    return ' #NUMBER# '

def replace_nmbrr(match) :
    return '#NUMBER#'


def string_to_number(S) :
    pattern = r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)\s+"
    S = re.sub(pattern, ' #NUMBER# ', S)

    pattern = r"(#NUMBER#|#FRACTION#)+(-)?(#NUMBER#|#FRACTION#)"
    S = re.sub(pattern, '#NUMBER#', S)

    pattern = r"#NUMBER#.?#NUMBER#"
    S = re.sub(pattern, replace_nmbrr, S)

    pattern = r"#NUMBER#°[f|c]?"
    S = re.sub(pattern, '#TEMP#', S)

    pattern = r"\d+°[f|c]"
    S = re.sub(pattern, '#TEMP#', S)

    pattern = r"(minutes*|days*|hours*|seconds*|months*)"
    S = re.sub(pattern, '#TIME#', S)

    pattern = r"#NUMBER#\s+#TIME#"
    S = re.sub(pattern, '#DURATION#', S)

    pattern = r"(#NUMBER#|#FRACTION#)(\s+|-)(tbsps*|tsps*|cups*|bottles*|jugs*|mugs*|drops*|ounces*|oz|tablespoons*|teaspoons*|lbs*)(\.)*"
    S = re.sub(pattern, '#VOLUME#', S)

    pattern = r"#NUMBER#.?#NUMBER#"
    S = re.sub(pattern, '#NUMBER#', S)

    pattern = r"#NUMBER#\s+to\s+#DURATION#"
    S = re.sub(pattern, '#DURATION#', S)



    return S




def replace_word(match) :
    s = match.group(0)
    if s.startswith('tsp') or s.startswith('tbsp') or s.startswith('teaspoon') :
        s = 'tsp'
    return s 



def match_words(S) :
    pattern = r"(tsps*|tbsps*|teaspoons*)\.?"
    S = re.sub(pattern,replace_word,S)
    return S




if __name__ == '__main__' :
    import read_corpus

    S = 'place a rack in middle and lower third of oven; preheat to 425°f. Also heat milk to 75°f.'
    S = re.sub(PATMATCH['temp'], FUNCMATCH['temp'], S)
    print(S)
    sys.exit(0) 


    for K in KEYS :
        S = re.sub(PATMATCH[K], FUNCMATCH[K], S)
    print(S)
    print(type(S))
    S = S.split('  --  ')
    print(S)
    print(type(S))
    print('')

    slist = read_corpus.read_sentences_from_string(S)
    WL = read_corpus.nltk_tokenize_sentences(slist)
    for wl in WL :
        print(wl)
        print('')

