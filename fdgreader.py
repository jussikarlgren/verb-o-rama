from logger import logger
import re
from verb import Verb

error = True
temptext = True

personalpronouns = ["he", 'she', "they", "we", "i"]   # omit "you" bc reasons

def dofdgfiles(filenamelist, targetlist, loglevel=False):
    logger("Starting FDG file processing ", loglevel)
    taglinepattern = re.compile("^<([\/\w]+)>\s*$")
    sgmllinepattern = re.compile("^\d+\s+<(\w+)>\s+<\w+>\s*$")  # <s> or <p> signify end of sentence or paragraph
    wordlinepattern = re.compile("^(\d+)\s+([\d\/\'\w]+)\s+([\d\/\w]+)\s+(\w+):>(\d+)\s+(.*)$")
    # 5	it	it	subj:>6	@SUBJ %NH PRON NOM SG3
    antalverbs = 0
    antalutterances = 0
    antalord = 0
    utterancelengths = {}
    adverblist = {}
    defsubj = {}
    verblist = {}
    antaldocuments = 0
    antaldifferentverbs = 0
    for fdgfilename in filenamelist:
        logger(fdgfilename, loglevel)

        with open(fdgfilename, errors="replace", encoding='utf-8') as fdgfile:
            notes = {}
            tokens = []
            itemindex = {}
            itemrole = {}
            itemtarget = {}
            onpoint = []
            seenindoc = {}
            gameon = False
            fdgline = fdgfile.readline()
            lineno = 0
            while fdgline:
                lineno += 1
                tag = taglinepattern.match(fdgline)
                eos = sgmllinepattern.match(fdgline)
                word = wordlinepattern.match(fdgline)
                if word:
                    antalord += 1
                    lemma = word.groups()[2]
                    surface = word.groups()[1]
                    position = word.groups()[0]
                    role = word.groups()[3]
                    head = word.groups()[4]
                    morph = word.groups()[5]
                    morphitems = morph.split()
                    tokens.append(lemma)
                    if gameon:
                        if (lemma in targetlist) and ("MAINV" in morph or "V" in morphitems):
                            onpoint.append(position)
                            if lemma in seenindoc:
                                seenindoc[lemma] += 1
                            else:
                                seenindoc[lemma] = 1
                            if lemma in verblist:
                                verblist[lemma].update()
                            else:
                                verblist[lemma] = Verb(lemma)
                                antaldifferentverbs += 1
                            if "+FMAINV" in morph:
                                verblist[lemma].mainverb += 1
                            elif "-FMAINV" in morph:
                                verblist[lemma].minusmainverb += 1
                            if "ING" in morphitems:
                                verblist[lemma].progressive += 1
                            elif "PAST" in morphitems:
                                verblist[lemma].past += 1
                            elif "PRES" in morphitems:
                                verblist[lemma].present += 1
                            elif "EN" in morphitems:
                                verblist[lemma].participle += 1
                            elif "INF" in morphitems:
                                verblist[lemma].infinitive += 1
                            elif "IMP" in morphitems:
                                verblist[lemma].imperative += 1
                            else:
                                verblist[lemma].othertenses += morph + ";"
                            antalverbs += 1
                        itemindex[position] = lemma
                        itemtarget[position] = head
                        itemrole[position] = role
                        if role == "subj" or role == "obj":
                            if position in itemtarget.values():
                                for attribute in itemtarget:
                                    if itemtarget[attribute] == position:
                                        if itemrole[attribute] == "det":
                                            if itemindex[attribute] == "a" or itemindex[attribute] == "an":
                                                notes[position] = "INDEFINITE"
                                            else:
                                                notes[position] = "DEFINITE"
                                        elif itemindex[attribute] in personalpronouns:
                                            notes[position] = "PERSONALPRONOUN"
                elif tag:
                    if (tag.groups()[0] == "HEADLINE" or tag.groups()[0] == "TEXT"):
                        gameon = True
                    if (tag.groups()[0] == "/HEADLINE" or tag.groups()[0] == "/TEXT"):
                        gameon = False
                    if tag.groups()[0] == "/DOC":
                        for pointverb in seenindoc:
                            verblist[pointverb].antaldocuments += 1
                            if seenindoc[pointverb] > 1:
                                verblist[pointverb].antaldocumentsmultipleoccurrences += 1
                        seenindoc = {}
                        antaldocuments += 1
                elif eos:  # end of sentence or paragraph
                    antalutterances += 1
                    for pointverbposition in onpoint:
                        if temptext:
                            print(itemindex[pointverbposition], end="\t")
                        pointverb = itemindex[pointverbposition]
                        for attribute in itemtarget:
                            if itemtarget[attribute] == pointverbposition:

                                if itemrole[attribute] == "neg":  # negation
                                    verblist[pointverb].negation += 1
                                if temptext:
                                    print("NOT", end="\t")
                                else:
                                    print("\t", end="\t")
                                if itemrole[attribute] == "tmp":  # temporal adverb or construction
                                    verblist[pointverb].tmpadverbs += 1
                                if temptext:
                                    print(itemindex[attribute], end="\t")
                                if itemrole[attribute] == "man":  # manner adverb or construction
                                    verblist[pointverb].manadverbs += 1
                                    if temptext:
                                        print(itemindex[attribute], end="\t")
                                if itemrole[attribute] == "meta" or itemrole[attribute] == "ad" \
                                        or itemrole[attribute] == "ha":
                                    verblist[pointverb].adverbs += 1
                                    if temptext:
                                        print(itemindex[attribute], end="\t")
                                if itemindex[attribute] == "here" or itemindex[attribute] == "now":
                                    verblist[pointverb].herenow += 1
                                if itemrole[attribute] == "subj":
                                    try:
                                        if notes[attribute] == "DEFINITE":
                                            verblist[pointverb].definitesubject += 1
                                        if notes[attribute] == "INDEFINITE":
                                            verblist[pointverb].indefinitesubject += 1
                                        if notes[attribute] == "PERSONALPRONOUN":
                                            verblist[pointverb].personalpronounsubject += 1
                                    except KeyError:
                                        pass
                        if temptext:
                            print("\n")
                        verblist[pointverb].utterancelengths += len(tokens)
                        verblist[pointverb].antalutterances += 1
                    tokens = []
                    itemindex = {}
                    itemtarget = {}
                    itemrole = {}
                    notes = {}
                    onpoint = []
                try:
                    fdgline = fdgfile.readline()
                except UnicodeDecodeError:
                    logger("file error "+fdgfilename+" "+fdgline)
                    fdgline = fdgfile.readline()

            logger(str(antalverbs) + " verbs seen; " + str(antaldifferentverbs) + " different verbs; " +
                   str(antaldocuments) + " documents seen; " +
                   str(antalutterances) + " utterances seen; " + str(antalord) +
                   " words seen" , loglevel)

    return verblist
            # adv positions
            # position in clause
            # verb particles
            # tense
            # aux attachments
            # katz stats
