from collections import Counter

import pymorphy2
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
import re
import string
import math


def parseFileToDict(file):
    d = dict()
    for line in file.readlines():
        strings = line.split('\n')[0].split(': ')
        k = strings[0]
        other = strings[1].strip().split(' ')
        d[k] = []
        for i in other:
            d[k].append(i)
    file.close()
    return d


class Task4:

    def __init__(self):
        self.resourcesPath = '/Users/angelina/PycharmProjects/InfSearch/resources/'
        self.invertedIndexFile = open(self.resourcesPath + 'invertedIndex.txt', 'r')
        self.lemmasFile = open(self.resourcesPath + 'lemmas.txt', 'r')
        self.lemmas = parseFileToDict(self.lemmasFile)
        self.invertedIndex = parseFileToDict(self.invertedIndexFile)
        self.morph = pymorphy2.MorphAnalyzer()

    def isCorrectToken(self, token):
        if any(x in string.punctuation for x in token): return False
        if bool(re.compile(r'^[0-9]+$').match(token)): return False
        if bool(re.compile(r'^[а-яА-Я]{2,}$').match(token)):
            return self.morph.parse(token)[0].score
        else:
            return False

    def createLemmas(self, tokens):
        l = list()
        for token in tokens:
            p = self.morph.parse(token)[0]
            normalForm = p.normal_form if p.normalized.is_known else token.lower()
            l.append(normalForm)
        return l

    def createFilesByFormulas(self, index):
        token_idf_tfidf = dict()
        lemma_idf_tfidf = dict()
        html = open('/Users/angelina/PycharmProjects/InfSearch/resources/pages/' + str(index) + '.txt', 'r',
                    encoding='utf-8')
        text = BeautifulSoup(html, features='html.parser').get_text()
        tokens = list(filter(self.isCorrectToken, wordpunct_tokenize(text)))
        counterTokens = Counter(tokens)
        html.close()
        lemmas = self.createLemmas(tokens)
        counterLemmas = Counter(lemmas)
        for key in self.invertedIndex.keys():
            if str(index) in self.invertedIndex[key]:
                all = len(self.invertedIndex[key])
                tmp_idf = math.log10(100 / all)
                for t in self.lemmas[key]:
                    if t in tokens:
                        tf = counterTokens[t] / len(tokens)
                        if t in token_idf_tfidf:
                            token_idf_tfidf[t].append(tmp_idf)
                        else:
                            token_idf_tfidf[t] = [tmp_idf]
                        token_idf_tfidf[t].append(tf * tmp_idf)
                        print(counterLemmas[key])
                lemma_tf = counterLemmas[key] / len(lemmas)
                if key in lemma_idf_tfidf:
                    lemma_idf_tfidf[key].append(tmp_idf)
                else:
                    lemma_idf_tfidf[key] = [tmp_idf]
                lemma_idf_tfidf[key].append(lemma_tf * tmp_idf)
        for key in token_idf_tfidf.keys():
            f = open('/Users/angelina/PycharmProjects/InfSearch/Task4/' + 'if-idf/token-index/' + str(index) + '.txt',
                     'a')
            f.write(key + ': ')
            for t in token_idf_tfidf[key]:
                f.write(str(t) + ' ')
            f.write('\n')
            f.close()
        for key in lemma_idf_tfidf.keys():
            f = open('/Users/angelina/PycharmProjects/InfSearch/Task4/' + 'if-idf/lemma-index/' + str(index) + '.txt',
                     'a')
            f.write(key + ': ')
            for t in lemma_idf_tfidf[key]:
                f.write(str(t) + ' ')
            f.write('\n')
            f.close()


if __name__ == '__main__':
    t4 = Task4()
    for i in range(0, 101):
        t4.createFilesByFormulas(i)
