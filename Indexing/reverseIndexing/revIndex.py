import re
from collections import defaultdict
from array import array
from bs4 import BeautifulSoup as BS
import csv

hitList = defaultdict(list)
textList = []

class HashTable:
    def __init__(self):
        pass

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
        self.readFiles()
        regex = ['<title>(.*?)</title>', '<id>(.*?)</id>|$', '<text xml:space="preserve">(.*?)</text>', '<text>(.*?)</text>']  # tags to parse
        wiki = open(self.filename, 'r')
        pageList = []
        for line in wiki:
            if line != "</page>":
                pageList.append(line)
            else:
                break
        simplewiki = ''.join(pageList)
        soup = BS(simplewiki, 'html.parser')
        for i in soup.findAll('text'):
           textList.append(i.text)

    def writeFile(self):
        myFile = open(self.csvFile, 'w')
        myFile.write('Key, DocIDs')
        myFile.write('\n')
        for key in hitList.iterkeys():
            temp = []
            for val in hitList[key]:
                docID = val[0]
                occurence = val[1]
                temp.append(':'.join([str(docID), ','.join(map(str,occurence))]))
                inStr = ''.join(temp)
                myFile.write(key+","+str(inStr)+"\n")
        myFile.close()
        
    def readFiles(self):
        self.filename = "simplewiki.dat"
        self.csvFile = "data.csv"
        self.grammerFile = "grammer.dat"

    def createhashtable(self):
        self.readFiles()
        self.wikiFile = self.filename
        self.parse()
        self.cleargrammer()
        for i in range(len(textList)):
            keys = self.getKeys(textList[i])
            invertedIndex = {}
            pID = i+1
            for value, key in enumerate(keys):
                try:
                    invertedIndex[key][1].append(value)
                except:
                    invertedIndex[key] = [pID, array('I', [value])]  # hashtable[id, [ArrayList]]
            for curPage, invPag in invertedIndex.iteritems():
                hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
            print "Done Doc ID: ", pID
        self.writeFile()

if __name__ == "__main__":
    invIndex = HashTable()
    invIndex.createhashtable()
