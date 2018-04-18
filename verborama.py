import re
import os
from fdgreader import dofdgfiles

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


monitor = True   # loglevel
debug = True


resourcedirectory = "/home/jussi/data/GH95-fdg/"

#  pronouns

#  mwu for sentence qualities, not averages

filenamelist = []

month = "\d\d"
day = "\d\d"
filenamepattern = "95" + month + day + "\.sgml\.fdg\.xml"
for filename in os.listdir(resourcedirectory):
    hitlist = re.match(filenamepattern, filename)
    if hitlist:
        filenamelist.append(os.path.join(resourcedirectory, filename))
verblist = dofdgfiles(filenamelist, thinkverbs + sayverbs, False)
sverblist = sorted(verblist.items(), key=lambda i: i[1].frequency, reverse=True)
for v in sverblist:
    if (v[1].frequency > 100):
        print(v[0], str(v[1]),

#
              sep="\t")
#    for verb in verblist:
#        print(verb,globalfrequency[verb],utterancelengths[verb],utterancelengths[verb]/globalfrequency[verb],adverblist[verb],adverblist[verb]/globalfrequency[verb],defsubj[verb],defsubj[verb]/globalfrequency[verb])
