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
    result = re.match(r'\d+?°[fc]', S)
    if result :
        result = 'TTEMPP' 
    else :
        result = 'UNK'

    return result 



def replace_time(match) :
    return 'TTIMEE'






PATMATCH = {}
FUNCMATCH = {}
KEYS = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp']

PATMATCH['fraction'] = r'([1-9]+/[1-9]+)'
PATMATCH['square_brace'] = r'(\[.*?\])'
PATMATCH['single_quote'] = r'(\'.*?\')' 
PATMATCH['linebreak'] = r'(\'\s*,\s*\'?)' 
PATMATCH['temp'] =  r'(\d+?°[fc])' 
PATMATCH['time'] =  r'(\d+ (\w* )*(minutes|days|hours))|(\w+ (minutes|days|hours))' 


FUNCMATCH['fraction'] = replace_fraction 
FUNCMATCH['square_brace'] = replace_square_brace
FUNCMATCH['single_quote'] = replace_single_quote 
FUNCMATCH['linebreak'] = replace_linebreak 
FUNCMATCH['temp'] = replace_temp 
FUNCMATCH['time'] = replace_time 



def process_Ingredients(S) :
    IK = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp', 'time']
    for K in IK :
        S = re.sub(PATMATCH[K], FUNCMATCH[K], S)
    return S.split('  --  ')



def process_Instructions(S) :
    IK = ['linebreak', 'fraction', 'square_brace', 'single_quote', 'temp', 'time']
    for K in IK :
        S = re.sub(PATMATCH[K], FUNCMATCH[K], S)

    return S
    #return S.split('  --  ')




if __name__ == '__main__' :
    import read_corpus

    S = "['two pounds 1-inch pieces trimmed boneless veal stew meat', '1/4 cup all purpose flour', 'three tablespoons butter', 'one tablespoon olive oil', 'two medium onions, finely chopped', 'two celery stalks, finely chopped', 'one 1/four cups dry white wine', 'two cups tomato sauce', 'one cup (or more) water', 'three tablespoons chopped fresh parsley', 'two cinnamon sticks', 'one 1/4 pounds white-skinned potatoes, peeled, cut into 1/2-inch pieces', '1/2 cup whipping cream']"

    S = r"['one (3 onehalf–4-lb.) whole chicken', '2 threefourth tsp. kosher salt, divided, plus more', 'two small acorn squash (about three lb. total)', 'two Tbsp. finely chopped sage', 'one Tbsp. finely chopped rosemary', 'six Tbsp. unsalted butter, melted, plus three Tbsp. room temperature', ' onefourth tsp. ground allspice', 'Pinch of crushed red pepper flakes', 'Freshly ground black pepper', ' onethird loaf good-quality sturdy white bread, torn into 1 pieces (about 2 onehalf cups)', 'two medium apples (such as Gala or Pink Lady; about 14 oz. total), cored, cut into 1 pieces', 'two Tbsp. extra-virgin olive oil', ' onehalf small red onion, thinly sliced', 'three Tbsp. apple cider vinegar', 'one Tbsp. white miso', ' onefourth cup all-purpose flour', 'two Tbsp. unsalted butter, room temperature', ' onefourth cup dry white wine', 'two cups unsalted chicken broth', 'two tsp. white miso', 'Kosher salt, freshly ground pepper']"


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

