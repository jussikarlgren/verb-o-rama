class Verb:
    def __init__(self, lemma):
        self.frequency = 1
        self.adverbs = 0
        self.past = 0
        self.progressive = 0
        self.present = 0
        self.participle = 0
        self.aux = 0
        self.finitemain = 0
        self.question = 0
        self.imperative = 0
        self.passive = 0
        self.active = 0
        self.definitesubject = 0
        self.indefinitesubject = 0
        self.personalpronounsubject = 0
        self.itsubject = 0
        self.lemma = lemma
        self.utterancelengths = 0
        self.antalutterances = 0
        self.antaldocuments = 0
        self.othertenses = ""
        self.infinitive = 0
        self.tmpadverbs = 0
        self.manadverbs = 0
        self.herenow = 0
        self.negation = 0
        self.antaldocumentsmultipleoccurrences = 0
        self.mainverb = 0
        self.minusmainverb = 0

    def update(self):
        self.frequency += 1

    def adverbiallistupdate(self, adverbs):
        self.adverbs += len(adverbs)

    def adverbialupdate(self, adverb):
        self.adverbs += 1

    def katzgamma(self):
        return self.antaldocumentsmultipleoccurrences/self.antaldocuments

    def katzburst(self):
        if self.antaldocumentsmultipleoccurrences > 0:
            return (self.frequency - (self.antaldocuments - self.antaldocumentsmultipleoccurrences)) / \
                   self.antaldocumentsmultipleoccurrences
        else:
            return 0

    def __str__(self):
        response = str(self.lemma) + "\t" + str(self.frequency) + "\t" + str(self.antaldocuments) + "\t" + \
                   str(self.katzgamma()) +  "\t" +  str(self.katzburst()) +  "\t" + \
                   str(self.negation / self.frequency) +  "\t" +  str(self.adverbs / self.frequency) +  \
                   "\t" +  str(self.tmpadverbs / self.frequency) +  "\t" +  str(self.manadverbs / self.frequency) +  \
                   "\t" +  str(self.present / self.frequency) +  "\t" +  str(self.past / self.frequency) +  "\t" + \
                   str(self.participle / self.frequency) +  "\t" +  str(self.progressive / self.frequency) +  "\t" +\
                   str(self.infinitive / self.frequency) +  "\t" +  str(self.imperative / self.frequency) + "\t" + \
                   str(self.mainverb / self.frequency) + "\t" + str(self.minusmainverb / self.frequency)
        shortresponse = str(self.lemma) + "\t" + str(self.really) + "\t"
        return response
