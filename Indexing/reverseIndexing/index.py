import re
from collections import defaultdict
from array import array

# Helper lists and hashtable
pageList = []
cache = {}  # index of every word, hashtable
hitList = defaultdict(list)  # the total index of whole file.

# file links
filename = "/Users/Janjua/Desktop/BSCS/3rd Semester/DSA/Project/test.da"
grammerFile = "/Users/Janjua/Desktop/BSCS/3rd Semester/DSA/Project/grammer.dat"
indexFile = "/Users/Janjua/Desktop/BSCS/3rd Semester/DSA/Project/index.dat"

def parse():
    #|$ to get just the first match.
    regex = ['<title>(.*?)</title>', '<id>(.*?)</id>|$', '<text xml:space="preserve">(.*?)</text>']  # tags to parse
    wiki = open(filename, "r")
    for line in wiki:
        if line != "</page>\n":
            pageList.append(line)
        else:
            break
    simplewiki = ''.join(pageList)
    pTitle = re.search(regex[0], simplewiki, re.DOTALL)
    pText = re.search(regex[2], simplewiki, re.DOTALL)
    pID = re.search(regex[1], simplewiki, re.DOTALL)
    print "Creating hashtable!"
    cache['title'] = pTitle.group(1)
    cache['text'] = pText.group(1)
    cache['id'] = pID.group(1)
    print "Done!"
    return cache


def cleargrammer(grammerFile):
    gFile = open(grammerFile, 'r')
    grammerDoc = [line.strip('\n') for line in gFile]  # gets the list of the grammerFile we want to clear.
    return grammerDoc


def getKeys(textLine):
    textLine = textLine.lower()
    grammerDoc = cleargrammer(grammerFile)
    textLine = re.sub('[^0-9a-zA-Z]+', ' ', textLine)  # replace alphanumeric characters with spaces.
    textLine = [line for line in textLine if line not in grammerDoc]
    return textLine


def writefile():
    outFile = open(indexFile, 'w')
    for key in hitList.iterkeys():
        pL = []
        for val in hitList[key]:
            docID = val[0]
            occr = val[1]
            pL.append(':'.join([str(docID), ','.join(map(str,occr))]))
        print >> outFile, ''.join((key,'|',';'.join(pL)))
    outFile.close()


def createhashtable():
    data = {}
    data = parse()
    while data != {}:
        line = '\n'.join((data['title'], data['text']))  # joining text and title
        keys = getKeys(line)
        invertedIndex = {}
        pID = int(data['id'])
        for value, key in enumerate(keys):
            try:
                invertedIndex[key][1].append(value)
            except:
                invertedIndex[key] = [pID, array('I', [value])]  # hashtable[id, [ArrayList]]
        for curPage, invPag in invertedIndex.iteritems():
            if __name__ == '__main__':
                hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
        data = parse()  # repeat for next page.
    writefile()


if __name__ == '__main__':
    createhashtable()
