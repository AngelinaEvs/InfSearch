import warnings

import numpy as np
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymorphy2 import MorphAnalyzer
from scipy.spatial import distance


class VectorSearch:

    def __init__(self):
        self.resourcesPath = '/Users/angelina/PycharmProjects/InfSearch/resources'
        self.urlsFile = open(self.resourcesPath + '/urls.txt', 'r', encoding='utf-8')
        self.tfidfDir = '/Users/angelina/PycharmProjects/InfSearch/Task4/if-idf/lemma-index/'
        self.urls = self.parseUrlsFile()
        self.lemmas = []
        self.matrix = None
        self.parseLemmaIndexFile()
        self.parseTfIdf()
        self.morph = MorphAnalyzer()

    def parseUrlsFile(self):
        arr = []
        for line in self.urlsFile.readlines():
            arr.append(line)
        self.urlsFile.close()
        return arr

    def parseLemmaIndexFile(self):
        for i in range(0, 100):
            f = open(self.tfidfDir + str(i) + '.txt', 'r', encoding='utf-8')
            for line in f.readlines():
                self.lemmas.append(line.split(':')[0])

    def parseTfIdf(self):
        self.matrix = np.zeros((100, len(self.lemmas)))
        for i in range(0, 100):
            f = open(self.tfidfDir + str(i) + '.txt', 'r', encoding='utf-8')
            lines = f.readlines()
            for j in range(len(lines)):
                tfIdf = float(lines[j].split(': ')[1].split(' ')[1])
                self.matrix[i][j] = tfIdf
            f.close()

    def vector(self, q: str) -> np.ndarray:
        v = np.zeros(len(self.lemmas))
        print(q)
        tokens = q.split(' ')
        for token in tokens:
            parsedToken = self.morph.parse(token)[0]
            lemma = parsedToken.normal_form if parsedToken.normalized.is_known else token.lower()
            if lemma in self.lemmas:
                v[self.lemmas.index(lemma)] = 1
        return v

    def search(self, q: str) -> list:
        v = self.vector(q)
        similarities = dict()
        i = 1
        for row in self.matrix:
            d = 1 - distance.cosine(v, row)
            if d > 0:
                similarities[i] = d
            i = i + 1
        sortedSimil = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        result = [(self.urls[doc[0]], doc[1]) for doc in sortedSimil]
        return result


templates = Jinja2Templates('/Users/angelina/PycharmProjects/InfSearch/Task5/')
app = FastAPI()
vector = VectorSearch()
warnings.filterwarnings('ignore')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request, q: str = ''):
    result = []
    if q:
        result = vector.search(q)
    return templates.TemplateResponse('index.html', context={'request': request, 'result': result, 'q': q})


if __name__ == '__main__':
    uvicorn.run(app)
    # result = vector.search('настройка технический')
    # print(result)