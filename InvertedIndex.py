import pymorphy2
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize


class InvertedIndex:

    def __init__(self):
        self.resourcesPath = '/Users/angelina/PycharmProjects/InfSearch/resources/'
        self.lemmasFile = open(self.resourcesPath + 'lemmas.txt', 'r', encoding='utf-8')
        self.infinitive = dict()
        self.infinitiveIndex = dict()
        self.invertedIndexFile = open(self.resourcesPath + 'invertedIndex.txt', 'w')
        self.morph = pymorphy2.MorphAnalyzer()

    def getInfinitiveFromLemmas(self):
        for line in self.lemmasFile.readlines():
            lineSplit = line.split('\n')[0].split(': ')
            inf = lineSplit[0]
            other = lineSplit[1].split(' ')
            self.infinitiveIndex[inf] = list()
            self.infinitive[inf] = other
        self.lemmasFile.close()

    def checkFiles(self):
        pagesPath = self.resourcesPath + 'pages/'
        for i in range(0, 100):
            file = open(pagesPath + str(i) + '.txt', 'r', encoding='utf-8')
            body = BeautifulSoup(file, features='html.parser').get_text()
            wordList = wordpunct_tokenize(body)
            words = set()
            for word in wordList:
                wordInfo = self.morph.parse(word)[0]
                normalForm = wordInfo.normal_form if wordInfo.normalized.is_known else word.lower()
                if normalForm in self.infinitive.keys() and normalForm not in words:
                    words.add(normalForm)
                    self.infinitiveIndex[normalForm].append(i)
            file.close()
        for key, value in self.infinitiveIndex.items():
            value.sort()

    def writeIndexToFile(self):
        for key, value in self.infinitiveIndex.items():
            vstring = ""
            for v in value:
                vstring = vstring + str(v) + ' '
            s = key + ': ' + vstring + '\n'
            self.invertedIndexFile.write(s)
        self.invertedIndexFile.close()


if __name__ == '__main__':
    invertedIndex = InvertedIndex()
    invertedIndex.getInfinitiveFromLemmas()
    invertedIndex.checkFiles()
    invertedIndex.writeIndexToFile()
