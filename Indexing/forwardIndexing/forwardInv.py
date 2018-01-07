import re
from collections import defaultdict, OrderedDict

grammerFile = 'grammer.dat'

class ForwardIndex:
    def __init__(self):
        pass

    hitlist = defaultdict(list)
    strArr = ['Hello', 'How are you', 'Kamran Janjua',
              'Mandela was a great leader. He revolunized the whole South Africa',
              'I love Mandela, he was a great leader',
              'Cricket is the best game in England.',
              'The most important month of the year is April, April is important.',
              'This string contains duplicates. This string contains duplicates. This string contains DUPLICATES',
              'ANOTHER TEST DOCUMENT, SEEEEEEEEEEEEH HOW THIS WORKS',
              'The CPU pushes the Flags Register onto the stack. The CPU pushes a far return address (segment: offset) onto the stack, segment value first. The CPU determines the cause of the interrupt (i.e., the interrupt vector number) and fetches the four byte interrupt vector from address 0:vector*4. The CPU transfers control to the routine specified by the interrupt vector table entry']

    def cleargrammer(self):
        gFile = open(grammerFile, 'r')
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

    def main(self):
        for i in range(len(self.strArr)):
            line = self.getkeys(self.strArr[i])
            pID = i+1
            self.hitlist[pID] = line
            print "Done DocID: ", pID

if __name__ == '__main__':
    fInd = ForwardIndex()
    fInd.main()
    for docID in fInd.hitlist.iterkeys():
        print "Doc ID: ", docID, " ", "Words: ", fInd.hitlist[docID]
