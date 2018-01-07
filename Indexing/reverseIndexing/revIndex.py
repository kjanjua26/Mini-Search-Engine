import re
from collections import defaultdict
from array import array
from bs4 import BeautifulSoup as BS
import csv
from tqdm import tqdm

hitList = defaultdict(list)
textList = []
titles = []

class HashTable:
    def __init__(self, source, grammerFile, output):
        self.filename = source
        self.csvFile = output
        gFile = open(grammerFile, 'r')
        self.grammerDoc = [line.strip('\n') for line in gFile]  # gets the list of the grammerFile we want to clear, strips the '\n'.

    def writeFile(self):
        myFile = open(self.csvFile, 'w')
        #for key in hitList.iterkeys(): # python 2.7
        for key in hitList.keys(): # python 3.x
            temp = []
            for val in hitList[key]:
                docID = val[0]
                occurence = val[1]
                temp.append(':'.join([str(docID), ','.join(map(str,occurence))]))
                inStr = ';'.join(temp)
                myFile.write(key+","+str(inStr)+"\n")
        myFile.close()
        
    def getKeys(self, textLine):
        line = re.sub('[^0-9a-zA-Z]+', ' ', textLine) #replaces the non-ASCII values with space
        line = line.split()
        line = [x for x in line if x not in self.grammerDoc]  # eliminate the articles, prepositions etc.
        return line

    def parse(self):
        wiki = open(self.filename, 'r', encoding="UTF-8")
        pageList = []
        print('Reading the corpus...');
        for line in wiki:
            if line != "</page>":
                pageList.append(line.lower()) # oomparisons are case sensitive so make all lower
            else:
                break

        simplewiki = ''.join(pageList)
        soup = BS(simplewiki, 'html.parser')

        for i in soup.findAll(['title']):
            titles.append(i.text)
        
        for i in soup.findAll(['text']):
            textList.append(i.text)

    def createhashtable(self):
        self.parse()
        print('Indexing...')
        for i in tqdm(range(len(textList))):
            invertedIndex = {}
            keys = self.getKeys(titles[i])
            for key in keys:
                try:
                    invertedIndex[key][1].append(0)
                except:
                    invertedIndex[key] = [i+1, array('I', [0])]  # hashtable[id, [ArrayList]]

            keys = self.getKeys(textList[i])
            for value, key in enumerate(keys):
                try:
                    invertedIndex[key][1].append(value+1)
                except:
                    invertedIndex[key] = [i+1, array('I', [value+1])]  # hashtable[id, [ArrayList]]

            #for curPage, invPag in invertedIndex.iteritems(): #python 2.7
            for curPage, invPag in invertedIndex.items(): #python 3.x
                hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
        self.writeFile()

if __name__ == "__main__":
    invIndex = HashTable("sample.dat", "grammer.rtf", "sampleData.csv")
    invIndex.createhashtable()