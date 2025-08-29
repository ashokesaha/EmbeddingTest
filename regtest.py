import re
import sys

pattern1 = r'\[(.*?)\]'
pattern2 = r'\((.*?)\)'
pattern3 = r'\'(.*?)\','


S = 'this is a [brace test] for running [red [shining tip] arrows]'

def mymatch(match) :
    grpn = len(match.groups())
    return match.group(1)


#while re.search(pattern, S) :
#    S = re.sub(pattern,mymatch,S)
#    print(S)


with open(sys.argv[1], 'r') as f :
    for line in f:
        while re.search(pattern1, line) :
            line = re.sub(pattern1, mymatch, line)

        while re.search(pattern2, line) :
            line = re.sub(pattern2, mymatch, line)

        while re.search(pattern3, line) :
            line = re.sub(pattern3, mymatch, line)

        print(line)
