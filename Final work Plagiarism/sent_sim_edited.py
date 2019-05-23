import argparse
from difflib import SequenceMatcher
import InvertedIndexSearch as isis
import re


parser = argparse.ArgumentParser(description='Find similar text between two documents.')
# parser.add_argument('-1', dest='d1', help='Text document 1', required=True)
# parser.add_argument('-2', dest='d2', help='Text document 2', required=True)
parser.add_argument('-k', dest='k', type=int, default=20, help='The number of char for 1st pass. Default 20')
parser.add_argument('-e', dest='ext', type=int, default=70, help='The number of additional char. Default 70')
parser.add_argument('-s', dest='minsim', type=float, default=.8, help='The minimum similarity to define a match. Default 0.8')
parser.add_argument('-tex', dest='tex', action='store_true', help='Skip LaTeX header and lines starting with %%')
args = parser.parse_args()

spacere = re.compile(' +')

# Read doc 1
def process_file(filename):
    all = ''
    header = False
    for line in open(filename, "r", encoding='utf8', errors='ignore'):
        if('begin{document}' in line):
            header = True
            break
    for line in open(filename, "r", encoding='utf8', errors='ignore'):
        if('begin{document}' in line):
            header = False
        if(args.tex and header):
            continue
        if(args.tex and line[0] == '%'):
            continue
        line = line.replace('\n', ' ')
        all += spacere.sub(" ", line)
    km = {}
    for pos in range(len(all)-args.k):
        km[all[pos:(pos+args.k)]] = pos
        
    return all, km

# Read doc 2

listz = isis.InvertedIndexSearch()
print(listz)

for i in range(0,len(listz)-1):
    name = "X/"+str(listz[len(listz)-1-i])+".txt"
    print(name)
    all1, km1 = process_file(name)
    all2, km2 = process_file('Test_document.txt')

    # Find common kmers
    kms = []
    for km in km1.keys():
        if(km in km2):
            kms.append(km)
    
    # Extend characters
    hits1 = []
    for km in kms:
        pos1 = km1[km]
        s1 = max(0, pos1-args.ext)
        e1 = min(len(all1), pos1+args.ext)
        text1 = all1[s1:e1]
        pos2 = km2[km]
        s2 = max(0, pos2-args.ext)
        e2 = min(len(all2), pos2+args.ext)
        text2 = all2[s2:e2]
        score = SequenceMatcher(None, text1, text2).ratio()
        if(score > args.minsim):
            hits1.append([pos1, round(score, 4), text1, text2, pos2])
    
    # Print non-overlapping hits
    hits1 = sorted(hits1, key=lambda hit: hit[0])
    curpos = -2 * args.ext
    for hit in hits1:
        if(hit[0] - curpos > 2*args.ext):
            curpos = hit[0]
            print('\nS:' + str(hit[1]))
            print('T1: ' + hit[2])
            print('T2: ' + hit[3])
    