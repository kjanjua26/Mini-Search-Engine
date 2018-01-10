from collections import defaultdict
from matplotlib import pyplot as plt
from tqdm import tqdm
from bs4 import BeautifulSoup as BS

wikiFile = 'sample.dat'
class Freq:

    textDict = defaultdict(list)
    myList = list()
    textList = []
    ids = []
    dic = {}

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

        self.myList = [words for segments in self.textList for words in segments.split()]
        for x in self.myList:
            if not x in self.dic:
                self.dic[x] = self.myList.count(x)
        print self.dic

    def plot(self):
        plt.bar(range(len(self.dic)), list(self.dic.values()), align='center')
        plt.xticks(range(len(self.dic)), list(self.dic.keys()))
        plt.show()

if __name__ == '__main__':
    instance = Freq()
    instance.countWords()
    instance.plot()
