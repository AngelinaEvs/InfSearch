!pip install pymorphy2
!pip install pymorphy2-dicts
!pip install DAWG-Python

import nltk
import string
import re
import pymorphy2
from os import listdir, path
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

class TokenCreator:

  def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokens = set()
        self.lemmas = dict()

  def isCorrectToken(self, token):
    if any(x in string.punctuation for x in token): return False 
    if bool(re.compile(r'^[0-9]+$').match(token)): return False
    if bool(re.compile(r'^[а-яА-Я]{2,}$').match(token)):
      return self.morph.parse(token)[0].score
    else:
       return False

  def createTokenList(self):
    html = open('/content/sample_data/ex.txt', 'r', encoding = 'utf-8')
    text = BeautifulSoup(html, features='html.parser').get_text()
    tokenArray = wordpunct_tokenize(text)
    self.tokens = self.tokens | set(filter(self.isCorrectToken, tokenArray))
    html.close()

  def createLemmas(self):
    for token in self.tokens:
      p = self.morph.parse(token)[0]
      normalForm = p.normal_form if p.normalized.is_known else token.lower()
      if normalForm not in self.lemmas:
        self.lemmas[normalForm] = []
      self.lemmas[normalForm].append(token)
    self.writeLemmasList() 

  def writeLemmasList(self):
    file = open('/content/sample_data/lemmas.txt', 'w')
    for lemma, tokens in self.lemmas.items():
      s = lemma + ': '
      for token in tokens:
        s = s + token + ' '
      s = s + '\n'
      file.write(s)
    file.close()        

if __name__ == '__main__':
  tokenCreator = TokenCreator()
  tokenCreator.createTokenList()
  tokenCreator.createLemmas()
