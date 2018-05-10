import sparsevectors
import math
from logger import logger
import pickle

error = True
debug = False
monitor = False


class VerbSpace:
    def __init__(self, dimensionality=2000, denseness=10):
        self.indexspace = {}
        self.contextspace = {}
        self.morphologyspace = {}
        self.attributespace = {}
        self.globalfrequency = {}
        self.bign = 0
        self.dimensionality = dimensionality
        self.denseness = denseness
        self.permutationcollection = {}
        self.constantcollection = {}
        self.category = {}
        self.name = {}

    def items(self):
        return self.indexspace.keys()

    def addoperator(self, item):
        self.permutationcollection[item] = sparsevectors.createpermutation(self.dimensionality)

    def addconstant(self, item):
        self.constantcollection[item] = sparsevectors.newrandomvector(self.dimensionality, self.denseness)

    def contains(self, item):
        if item in self.indexspace:
            return True
        else:
            return False

    def checkwordspacelist(self, words, loglevel=False):
        for word in words:
            self.checkwordspace(word, loglevel)

    def checkwordspace(self, word, loglevel=False):
        self.bign += 1
        if self.contains(word):
            self.globalfrequency[word] += 1
        else:
            self.additem(word)
            logger(str(word) + " is new and now hallucinated: " + str(self.indexspace[word]), loglevel)

    def observe(self, item):
        self.globalfrequency[item] += 1

    def additem(self, item, vector="dummy"):
        if vector is "dummy":
            vector = sparsevectors.newrandomvector(self.dimensionality, self.denseness)
        if not self.contains(item):
            self.indexspace[item] = vector
            self.globalfrequency[item] = 1
            self.contextspace[item] = sparsevectors.newemptyvector(self.dimensionality)
            self.attributespace[item] = sparsevectors.newemptyvector(self.dimensionality)
            self.morphologyspace[item] = sparsevectors.newemptyvector(self.dimensionality)
#            self.textspace[item] = sparsevectors.newemptyvector(self.dimensionality)
#            self.utterancespace[item] = sparsevectors.newemptyvector(self.dimensionality)
#            self.authorspace[item] = sparsevectors.newemptyvector(self.dimensionality)
            self.bign += 1

    def applyoperator(self, item, operator, constant, weight):
        self.contextspace[item] = sparsevectors.sparseadd(
            self.contextspace[item],
            sparsevectors.normalise(sparsevectors.permute(self.constantcollection[constant],
                                                          self.permutationcollection[operator])),
            weight)
        if operator == "morphology":
                    self.morphologyspace[item] = sparsevectors.sparseadd(
                        self.morphologyspace[item],
                        sparsevectors.normalise(sparsevectors.permute(self.constantcollection[constant],
                        self.permutationcollection[operator])),
                        weight)
        else:
            self.attributespace[item] = sparsevectors.sparseadd(
                self.attributespace[item],
                sparsevectors.normalise(sparsevectors.permute(self.constantcollection[constant],
                                                          self.permutationcollection[operator])),
                weight)

    def increment(self, verb):
        self.bign += verb.frequency
        if not self.contains(verb.lemma):
            self.additem(verb.lemma)
        self.globalfrequency[verb.lemma] += verb.frequency
        tense = "none"
        weight = 0
        if verb.progressive > 0:
            tense = "progressive"
            weight = verb.progressive
            self.applyoperator(verb.lemma, "morphology", tense, weight)

        if verb.past > 0:
            tense = "past"
            weight = verb.past
            self.applyoperator(verb.lemma, "morphology", tense, weight)
        if verb.present > 0:
            tense = "present"
            weight = verb.present
            self.applyoperator(verb.lemma, "morphology", tense, weight)


        if verb.participle > 0:
            tense = "participle"
            weight = verb.participle
            self.applyoperator(verb.lemma, "morphology", tense, weight)


        if verb.adverbs > 0:
            self.applyoperator(verb.lemma, "adverb", "adverb", verb.adverbs)

        if verb.manadverbs > 0:
            self.applyoperator(verb.lemma, "adverb", "manner", verb.manadverbs)

        if verb.tmpadverbs > 0:
            self.applyoperator(verb.lemma, "adverb", "temporal", verb.tmpadverbs)
        if verb.negation > 0:
            self.applyoperator(verb.lemma, "mode", "negation", verb.negation)
        if verb.herenow > 0:
            self.applyoperator(verb.lemma, "adverb", "herenow", verb.herenow)


#        self.aux = 0
#        self.finitemain = 0
##        self.question = 0
##        self.imperative = 0
 #       self.passive = 0
 ##       self.active = 0
  #      self.definitesubject = 0
  #      self.indefinitesubject = 0
  #      self.personalpronounsubject = 0
  #      self.itsubject = 0
  #      self.utterancelengths = 0
  #      self.antalutterances = 0
  #      self.antaldocuments = 0
  #      self.othertenses = ""
  #      self.infinitive = 0
  #      self.antaldocumentsmultipleoccurrences = 0
  #      self.mainverb = 0
  #      self.minusmainverb = 0

    def addsaveditem(self, jsonitem):
        try:
            if self.contains(jsonitem["string"]):
                logger("Conflict in adding new item--- will clobber "+jsonitem["string"], error)
            item = jsonitem["string"]
            self.indexspace[item] = jsonitem["indexvector"]
            self.globalfrequency[item] = int(jsonitem["frequency"])
            self.contextspace[item] = jsonitem["contextvector"]
            self.associationspace[item] = jsonitem["associationvector"]
            self.bign += int(jsonitem["frequency"])
        except:
            logger("Something wrong with item "+jsonitem, error)

    def frequencyweight(self, word):
        try:
            w = 1 - math.atan(self.globalfrequency[word] - 1) / (0.5 * math.pi)  # ranges between 1 and 1/3
        except KeyError:
            w = 0.5
        return w

    def outputwordspace(self, filename):
        with open(filename, 'wb') as outfile:
            for item in self.indexspace:
                try:
                    itemj = {}
                    itemj["string"] = str(item)
                    itemj["indexvector"] = self.indexspace[item]
                    itemj["contextvector"] = self.contextspace[item]
                    itemj["associationvector"] = self.associationspace[item]
                    itemj["frequency"] = self.globalfrequency[item]
                    pickle.dump(itemj, outfile)
                except TypeError:
                    logger("Could not write >>" + item + "<<", error)

    def importstats(self, wordstatsfile):
        with open(wordstatsfile) as savedstats:
            i = 0
            for line in savedstats:
                i += 1
                try:
                    seqstats = line.rstrip().split("\t")
                    if not self.contains(seqstats[0]):
                        self.additem(seqstats[0])
                    self.globalfrequency[seqstats[0]] = int(seqstats[1])
                    self.bign += int(seqstats[1])
                except IndexError:
                    logger("***" + str(i) + " " + line.rstrip(), debug)

    def importindexvectors(self, indexvectorfile, frequencythreshold=0):
        cannedindexvectors = open(indexvectorfile, "rb")
        goingalong = True
        n = 0
        m = 0
        while goingalong:
            try:
                itemj = pickle.load(cannedindexvectors)
                item = itemj["string"]
                indexvector = itemj["indexvector"]
                if not self.contains(item):
                    self.additem(item, indexvector)
                    n += 1
                else:
                    if self.globalfrequency[item] > frequencythreshold:
                        self.indexspace[item] = indexvector
                        m += 1
            except EOFError:
                goingalong = False
        return n, m

    def reducewordspace(self, threshold=1):
        items = list(self.indexspace.keys())
        for item in items:
            if self.globalfrequency[item] <= threshold:
                self.removeitem(item)

    def removeitem(self, item):
        if self.contains(item):
            del self.indexspace[item]
            del self.contextspace[item]
            del self.associationspace[item]
            del self.globalfrequency[item]
            self.bign -= 1

    def newemptyvector(self):
        return sparsevectors.newemptyvector(self.dimensionality)

    def similarity(self, item, anotheritem):
        return sparsevectors.sparsecosine(self.contextspace[item], self.contextspace[anotheritem])
    def similarityA(self, item, anotheritem):
        return sparsevectors.sparsecosine(self.attributespace[item], self.attributespace[anotheritem])
    def similarityM(self, item, anotheritem):
        return sparsevectors.sparsecosine(self.morphologyspace[item], self.morphologyspace[anotheritem])

