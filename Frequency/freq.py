import re
import zlib
from collections import defaultdict
from matplotlib import pyplot as plt
from collections import Counter
from tqdm import tqdm
from bs4 import BeautifulSoup as BS

wikiFile = '' # wikipedia file.
class Freq:

    textDict = defaultdict(list)
    myList = list()
    textList = []
    ids = []

    def __init__(self):
        pass

    def parse(self):
        corpus = open(wikiFile, 'r')
        pageList = []
        print('Reading the corpus...')
        for line in tqdm(corpus):
            pageList.append(line.strip().lower())  # comparisons are case sensitive so make all lower

        soup = BS(' '.join(pageList), 'html.parser')

        print('\nParsing IDs...')
        for i in tqdm(soup.select('page > id')):
            self.ids.append(i.text)

        print('\nParsing Text...')
        for i in tqdm(soup.findAll('text')):
            self.textList.append(i.text)

    def countWords(self):
        self.parse()
        dic = {}
        self.myList = [words for segments in self.myList for words in segments.split()]
        for x in self.myList:
            if not x in dic:
                dic[x] = self.myList.count(x)
        print dic
        return dic

if __name__ == '__main__':
    instance = Freq()
    instance.countWords()
