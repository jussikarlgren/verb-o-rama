import re
import os
from fdgreader import dofdgfiles
import verbspace
from logger import logger

motionverbs = ["shuffle", "stumble", "dodder", "lope", "stroll", "jog", "wander", "amble", "saunter", "strut", "spurt",
               "stride", "scurry", "dart", "traipse", "drift", "waltz", "sashay", "pace", "sink", "rise", "move",
               "walk", "run", "leap", "skip", "hop", "jump", "slide", "slip", "fall", "tumble", "roll", "glide",
               "plummet", "tumble", "plunge", "slump", "rebound", "dive", "waver", "soar", "retreat", "wobble",
               "bounce", "falter", "seesaw"]

thinkverbs = ["think", "believe", "expect", "imagine", "anticipate", "surmise", "suppose", "conjecture", "guess",
              "conclude", "determine", "reason", "reckon", "figure", "opine", "deem", "assess", "judge", "hold",
              "reckon", "consider", "presume", "estimate", "ponder", "reflect", "deliberate", "meditate", "contemplate",
              "muse", "cogitate", "ruminate", "brood", "concentrate", "cerebrate", "consider", "contemplate",
              "deliberate", "mull", "muse", "recall", "remember", "recollect", "imagine", "picture", "visualize",
              "envisage", "envision", "dream", "fantasize", "suppose", "assume", "imagine", "presume", "hypothesis",
              "hypothesize", "postulate", "posit", "evaluate", "judge", "gauge", "rate", "estimate", "appraise",
              "analyse", "worry", "fret", "conceive"]
sayverbs = ["say", "speak", "utter", "voice", "pronounce", "vocalize", "declare", "state", "announce", "remark",
            "observe", "mention", "comment", "note", "add", "reply", "respond", "answer", "rejoin", "whisper", "mutter",
            "mumble", "mouth", "claim", "maintain", "assert", "hold", "insist", "contend", "aver", "affirm", "avow",
            "allege", "profess", "opine", "asseverate", "express", "phrase", "articulate", "communicate", "convey",
            "verbalize", "render", "tell", "reveal", "divulge", "impart", "disclose", "imply", "suggest", "signify",
            "denote", "mean", "recite", "repeat", "utter", "deliver", "perform", "declaim", "orate", "indicate",
            "estimate", "judge", "guess", "hazard a guess", "dare say", "predict", "speculate", "surmise", "conjecture",
            "venture", "pontificate", "propose", "plead", "mutter", "murmur", "mumble", "whisper", "hush", "grumble",
            "moan", "complain", "grouse", "carp", "whine", "bleat", "gripe", "whinge", "whine", "kvetch", "cry", "yelp",
            "call", "shout", "howl", "yowl", "wail", "scream", "shriek", "screech", "squawk", "squeal", "roar", "bawl",
            "whoop", "holler", "ululate", "laugh", "chuckle", "chortle", "guffaw", "giggle", "titter", "snigger",
            "snicker", "cackle", "howl", "roar", "smile", "ridicule", "mock", "deride", "scoff", "jeer", "sneer",
            "jibe", "scorn", "lampoon", "satirize", "caricature", "parody", "taunt", "tease", "torment", "expound",
            "declaim", "preach", "express", "sermonize", "moralize", "pronounce", "lecture", "expatiate", "spiel",
            "perorate"]
implicativeverbs = ["manage", "forget", "fail", "obey", "succeed"]

verbspace = verbspace.VerbSpace()
verbspace.addoperator("particle")
verbspace.addoperator("mode")
verbspace.addoperator("adverb")
verbspace.addoperator("morphology")
verbspace.addconstant("present")
verbspace.addconstant("negation")
verbspace.addconstant("possible")
verbspace.addconstant("amplify")
verbspace.addconstant("manner")
verbspace.addconstant("temporal")
verbspace.addconstant("adverb")
verbspace.addconstant("herenow")
verbspace.addconstant("past")
verbspace.addconstant("progressive")
verbspace.addconstant("participle")
verbspace.addconstant("none")  # stupid catchall

monitor = True   # loglevel
debug = False


resourcedirectory = "/home/jussi/data/GH95-fdg/"

#  pronouns

#  mwu for sentence qualities, not averages

filenamelist = []

month = "\d\d"
day = "\d\d"
filenamepattern = "95" + month + day + "\.sgml\.fdg\.xml"
for filenamecandidate in os.listdir(resourcedirectory):
    hitlist = re.match(filenamepattern, filenamecandidate)
    if hitlist:
        filenamelist.append(os.path.join(resourcedirectory, filenamecandidate))
logger(filenamelist, debug)
for filename in filenamelist:
    logger(filename, debug)
    verblist = dofdgfiles([filename], thinkverbs + sayverbs, debug)
    logger(str(len(verblist)), debug)
    for verb in verblist:
        verbspace.increment(verblist[verb])

top = 5
for v in verbspace.items():
    n = {}
    m = {}
    a = {}
    for w in verbspace.items():
        n[w] = verbspace.similarity(v, w)
        a[w] = verbspace.similarityA(v, w)
        m[w] = verbspace.similarityM(v, w)
    sverblist = sorted(verbspace.items(), key=lambda i: n[i], reverse=True)
    averblist = sorted(verbspace.items(), key=lambda i: a[i], reverse=True)
    mverblist = sorted(verbspace.items(), key=lambda i: m[i], reverse=True)
    best = sverblist[:top]
    worst = sverblist[-top:]
    besta = averblist[:top]
    worsta = averblist[-top:]
    bestm = mverblist[:top]
    worstm = mverblist[-top:]
    for u in best:
        logger(v + "\t\t" + u + "\t" + str(n[u]) + "\t" + str(verbspace.globalfrequency[v]) + "\t"
               + str(verbspace.globalfrequency[u]), monitor)

    for u in besta:
        logger(v + "\ta\t" + u + "\t" + str(a[u]) + "\t" + str(verbspace.globalfrequency[v]) + "\t"
               + str(verbspace.globalfrequency[u]), monitor)

    for u in bestm:
        logger(v + "\tm\t" + u + "\t" + str(m[u]) + "\t" + str(verbspace.globalfrequency[v]) + "\t"
               + str(verbspace.globalfrequency[u]), monitor)

    for u in worst:
        logger(v + "\t" + u + "\t" + str(n[u]) + "\t" + str(verbspace.globalfrequency[v]) + "\t"
               + str(verbspace.globalfrequency[u]), monitor)
