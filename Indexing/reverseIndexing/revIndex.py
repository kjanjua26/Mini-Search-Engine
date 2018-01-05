import re
from collections import defaultdict
from array import array

hitList = defaultdict(list)

class HashTable:
    def __init__(self):
        pass

    def cleargrammer(self):
        gFile = open(self.grammerFile, 'r')
        grammerDoc = [line.strip('\n') for line in gFile]  # gets the list of the grammerFile we want to clear, strips the '\n'.
        return grammerDoc

    def getKeys(self, textLine):
        gFile = self.cleargrammer()
        line = re.sub('[^0-9a-zA-Z]+', ' ', textLine) #replaces the non-ASCII values with *
        line = line.split()
        line = [x for x in line if x not in gFile]  # eliminate the articles, prepositions etc.
        return line

    def parse(self):
        # |$ to get just the first match.
        regex = ['<title>(.*?)</title>', '<id>(.*?)</id>|$', '<text xml:space="preserve">(.*?)</text>']  # tags to parse
        wiki = self.wikiFile
        pageList = []
        for line in wiki:
            if line != "</page>\n":
                pageList.append(line)
            else:
                break
        simplewiki = ''.join(pageList)
        pTitle = re.search(regex[0], simplewiki, re.DOTALL)
        pText = re.search(regex[2], simplewiki, re.DOTALL)
        pID = re.search(regex[1], simplewiki, re.DOTALL)
        if pTitle == None or pText == None or pID == None:
            return {}
        cache = {}
        print "Creating hashtable!"
        cache['title'] = pTitle.group(1)
        cache['text'] = pText.group(1)
        cache['id'] = pID.group(1)
        print "Done!"
        return cache

    def writeFile(self):
        f = open(self.outputFile, 'w')
        for key in hitList.iterkeys():
            temp = []
            for val in hitList[key]:
                docID = val[0]
                occurence = val[1]
                temp.append(':'.join([str(docID), ','.join(map(str,occurence))]))
                f.write(''.join((key,'|','->'.join(temp))))
        f.close()

    def readFiles(self):
        self.filename = "" #input wikipedia file
        self.grammerFile = "" #grammer file to remove the articles, prepositions etc.
        self.outputFile = "" #name of output file

    def createhashtable(self):
        self.readFiles()
        self.wikiFile = open(self.filename, 'r')
        self.cleargrammer()
        data = {}
        data = self.parse()
        while data != {}:
            line = '\n'.join((data['title'], data['text']))  # joining text and title
            keys = self.getKeys(line)
            invertedIndex = {}
            pID = int(data['id'])
            for value, key in enumerate(keys):
                try:
                    invertedIndex[key][1].append(value)
                except:
                    invertedIndex[key] = [pID, array('I', [value])]  # hashtable[id, [ArrayList]]

            for curPage, invPag in invertedIndex.iteritems():
                hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
            data = self.parse()  # repeat for next page.
        self.writeFile()


if __name__ == "__main__":
    invIndex = HashTable()
    invIndex.createhashtable()
