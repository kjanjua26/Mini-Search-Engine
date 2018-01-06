import re
from collections import defaultdict
from array import array
from bs4 import BeautifulSoup as BS
import csv
import time

hitList = defaultdict(list)
textList = []

class HashTable:
    def __init__(self, source, grammerFile, output):
        self.filename = source
        self.csvFile = output
        self.grammerFile = grammerFile

    def cleargrammer(self):
        gFile = open(self.grammerFile, 'r')
        grammerDoc = [line.strip('\n') for line in gFile]  # gets the list of the grammerFile we want to clear, strips the '\n'.
        return grammerDoc

    def getKeys(self, textLine):
        gFile = self.cleargrammer()
        line = re.sub('[^0-9a-zA-Z]+', ' ', textLine) #replaces the non-ASCII values with space
        line = line.split()
        line = [x for x in line if x not in gFile]  # eliminate the articles, prepositions etc.
        return line

    def parse(self):
        regex = ['<title>(.*?)</title>', '<id>(.*?)</id>|$', '<text xml:space="preserve">(.*?)</text>', '<text>(.*?)</text>']  # tags to parse
        wiki = open(self.filename, 'r', encoding="UTF-8")
        pageList = []
        print('Reading the corpus...');
        start = time.time()
        for line in wiki:
            if line != "</page>":
                pageList.append(line)
            else:
                break
        simplewiki = ''.join(pageList)
        soup = BS(simplewiki, 'html.parser')
        for i in soup.findAll('text'):
           textList.append(i.text)
        print('File read in: ', time.time() - start, ' sec')

    def writeFile(self):
        myFile = open(self.csvFile, 'w')
        myFile.write('Key, DocIDs')
        myFile.write('\n')
        #for key in hitList.iterkeys(): # python 2.7
        for key in hitList.keys(): # python 3.x
            temp = []
            for val in hitList[key]:
                docID = val[0]
                occurence = val[1]
                temp.append(':'.join([str(docID), ','.join(map(str,occurence))]))
                inStr = ''.join(temp)
                myFile.write(key+","+str(inStr)+"\n")
        myFile.close()
        
        

    def createhashtable(self):
        self.wikiFile = self.filename
        self.parse()
        self.cleargrammer()
        for i in range(len(textList)):
            start = time.time()
            keys = self.getKeys(textList[i])
            invertedIndex = {}
            pID = i+1
            for value, key in enumerate(keys):
                try:
                    invertedIndex[key][1].append(value)
                except:
                    invertedIndex[key] = [pID, array('I', [value])]  # hashtable[id, [ArrayList]]
            #for curPage, invPag in invertedIndex.iteritems(): #python 2.7
            for curPage, invPag in invertedIndex.items(): #python 3.x
                hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
            print("Done Doc ID: ", pID, ' IN: ', time.time() - start, ' sec')
        self.writeFile()

if __name__ == "__main__":
    invIndex = HashTable("simpleWiki.dat", "grammer.rtf", "data.csv")
    invIndex.createhashtable()