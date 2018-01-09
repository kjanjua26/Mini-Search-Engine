import re
from collections import defaultdict, OrderedDict
from tqdm import tqdm
from bs4 import BeautifulSoup as BS

class ForwardIndex:
    def __init__(self):
        pass

    hitlist = defaultdict(list)
    corpusFile = "scrappedOut.dat"
    grammerFile = 'grammer.dat'
    textList = []
    ids = []


    def parse(self):
        corpus = open(self.corpusFile, 'r')
        pageList = []
        print('Reading the corpus...')
        for line in tqdm(corpus):
            pageList.append(line.strip().lower())  # oomparisons are case sensitive so make all lower

        soup = BS(' '.join(pageList), 'html.parser')

        print('\nParsing IDs...')
        for i in tqdm(soup.select('page > id')):
            self.ids.append(i.text)

        print('\nParsing Text...')
        for i in tqdm(soup.findAll('text')):
            self.textList.append(i.text)

    def cleargrammer(self):
        gFile = open(self.grammerFile, 'r')
        grammerdoc = [line.strip('\n') for line in
                      gFile]  # gets the list of the grammerFile we want to clear, strips the '\n'.
        return grammerdoc

    def getkeys(self, textLine):
        gFile = self.cleargrammer()
        line = re.sub('[^0-9a-zA-Z]+', ' ', textLine)  # replaces the non-ASCII values with space
        line = line.lower()
        line = line.split()
        line = [x for x in line if x not in gFile]  # eliminate the articles, prepositions etc.
        line = list(OrderedDict.fromkeys(line)) #remove duplicates.
        return line

    def forIndex(self):
        self.parse()
        for i in (range(len(self.textList))):
            pID = self.ids[i]
            line = self.getkeys(self.textList[i])
            self.hitlist[pID] = line


if __name__ == '__main__':
    fInd = ForwardIndex()
    fInd.forIndex()
    for docID in fInd.hitlist.iterkeys():
        print "Doc ID: ", docID, " ", "Words: ", fInd.hitlist[docID]
