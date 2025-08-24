import re

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


S = "['two pounds 1-inch pieces trimmed boneless veal stew meat', '1/4 cup all purpose flour', 'three tablespoons butter', 'one tablespoon olive oil', 'two medium onions, finely chopped', 'two celery stalks, finely chopped', 'one 1/four cups dry white wine', 'two cups tomato sauce', 'one cup (or more) water', 'three tablespoons chopped fresh parsley', 'two cinnamon sticks', 'one 1/4 pounds white-skinned potatoes, peeled, cut into 1/2-inch pieces', '1/2 cup whipping cream']"

pat1 = r'(\w*)'
pat2 = r'([1-9]+/[1-9]+)'
pat3 = r'(\[.*?\])'

S = re.sub(pat3,replace_square_brace,S)
S = re.sub(pat2,replace_fraction,S)
print(S)
