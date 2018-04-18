from logger import logger
import re
import os

error = True

poses = ["N", "V", "A"]

def dofdgfiles(filenamelist, loglevel=False):
    global docstats, uttstats, antaldocuments, antalutterances, antalord, lexicalclass, seen, doctwicestats
    logger("Starting FDG file processing ", loglevel)
    taglinepattern = re.compile("^<([\/\w]+)>\s*$")
    sgmllinepattern = re.compile("^\d+\s+<(\w+)>\s+<\w+>\s*$")  # <s> or <p> signify end of sentence or paragraph
    wordlinepattern = re.compile("^(\d+)\s+([\d\/\'\w]+)\s+([\d\/\w]+)\s+(\w+):>(\d+)\s+(.*)$")
    # 5	it	it	subj:>6	@SUBJ %NH PRON NOM SG3
    lexicalclass = {}
    seen = {}
    docstats = {}
    doctwicestats = {}
    uttstats = {}
    for pos in poses:
        lexicalclass[pos] = 0
        seen[pos] = set()
        docstats[pos] = {}
        doctwicestats[pos] = {}
        uttstats[pos] = {}
    antalutterances = 0
    antalord = 0
    antaldocuments = 0
    utttokens = {}
    doctokens = {}
    doctwicetokens = {}
    for fdgfilename in filenamelist:
        logger(fdgfilename, loglevel)
        with open(fdgfilename, errors="replace", encoding='utf-8') as fdgfile:
            for pos in poses:
                utttokens[pos] = set()
                doctokens[pos] = set()
                doctwicetokens[pos] = set()
            gameon = False
            fdgline = fdgfile.readline()
            while fdgline:
                tag = taglinepattern.match(fdgline)
                eos = sgmllinepattern.match(fdgline)
                word = wordlinepattern.match(fdgline)
                if word:
                    antalord += 1
                    lemma = word.groups()[2]
                    morph = word.groups()[5]
                    morphitems = morph.split()
                    if gameon:
                        for onepos in poses:
                            if onepos in morphitems:
                                thispos = onepos
                                break
                        else:
                            thispos = None
                        if thispos:
                            lexicalclass[thispos] += 1
                            seen[thispos].add(lemma)
                            utttokens[thispos].add(lemma)
                            if lemma in doctokens[thispos]:
                                doctwicetokens[thispos].add(lemma)
                            else:
                                doctokens[thispos].add(lemma)
                elif tag:
                    if (tag.groups()[0] == "HEADLINE" or tag.groups()[0] == "TEXT"):
                        gameon = True
                    if (tag.groups()[0] == "/HEADLINE" or tag.groups()[0] == "/TEXT"):
                        gameon = False
                    if tag.groups()[0] == "/DOC":
                        antaldocuments += 1
                        for pos in poses:
                            for token in doctokens[pos]:
                                try:
                                    docstats[pos][token] += 1
                                except KeyError:
                                    docstats[pos][token] = 1
                            for token in doctwicetokens[pos]:
                                try:
                                    doctwicestats[pos][token] += 1
                                except KeyError:
                                    doctwicestats[pos][token] = 1
                            doctokens[pos] = set()
                            doctwicetokens[pos] = set()
                            for token in utttokens[pos]:
                                try:
                                    uttstats[pos][token] += 1
                                except KeyError:
                                    uttstats[pos][token] = 1
                                utttokens[pos] = set()
                elif eos:  # end of sentence or paragraph
                    antalutterances += 1
                for pos in poses:
                    for token in utttokens[pos]:
                        try:
                            uttstats[pos][token] += 1
                        except KeyError:
                            uttstats[pos][token] = 1
                    utttokens[pos] = set()
                try:
                    fdgline = fdgfile.readline()
                except UnicodeDecodeError:
                    logger("file error "+fdgfilename+" "+fdgline)
                    fdgline = fdgfile.readline()


resourcedirectories = ["/home/jussi/data/GH95-fdg/", "/home/jussi/data/LAT94-fdg"]

#  pronouns

#  mwu for sentence qualities, not averages

filenamelist = []

month = "\d\d"
day = "\d\d"
filenamepattern = "\d+" + month + day + "[\.\w]+\.xml"
for dir in resourcedirectories:
    for filename in os.listdir(dir):
        hitlist = re.match(filenamepattern, filename)
        if hitlist:
            filenamelist.append(os.path.join(dir, filename))
dofdgfiles(filenamelist, True)

uhistogram = {}
dhistogram = {}
d2histogram = {}

for pos in poses:
    dhistogram[pos] = {}
    for k in [100,200,500,1000,2000,5000,10000]:
        dhistogram[pos][k] = 0
        for v in docstats[pos]:
            if docstats[pos][v] > k:
                dhistogram[pos][k] += 1
for pos in poses:
    d2histogram[pos] = {}
    for k in [100,200,500,1000,2000,5000,10000]:
        d2histogram[pos][k] = 0
        for v in doctwicestats[pos]:
            if doctwicestats[pos][v] > k:
                d2histogram[pos][k] += 1

for a in poses:
    print(a, lexicalclass[a], len(seen[a]), dhistogram[a], d2histogram[a], sep="\t")
print("documents:", antaldocuments)
print("utterances:", antalutterances)
print("words:", antalord)
