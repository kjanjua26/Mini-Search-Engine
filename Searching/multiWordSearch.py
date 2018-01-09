import pickle
from collections import defaultdict
import time

pickleFile = "sampleP.pickle"


class Search:
    def __init__(self):
        pass

    hitList = defaultdict(list)

    def readPickle(self):
        pFile = open(pickleFile, 'rb')
        self.hitList = pickle.load(pFile)

    def search(self, query): # Single word searching.
        self.readPickle()
        try:
            docs = [x for x in self.hitList[query]]
            out = ''.join(map(str, docs))
        except:
            out = ''
        return out

    def singleWord(self, query):
        docs = self.search(query)
        try:
            print "The word is in: ", [x[0] for x in docs.split(';')] # gets the docs.
        except:
            print "\nThe term isn't in the docs!"

    def combine(self, list):
        return set().union(*list) # gets the union of all the lists.

    def doubleWord(self, query):
        dList = []
        query = query.split(' ')
        for term in query:
            docs = self.search(term)
            try:
                dList.append([x[0] for x in docs.split(';')]) #gets the docs.
            except:
                print "\nThe word that isn't in the docs is: ", term
        print "The words are in docs: ", self.combine(dList)

    def returnRes(self, query):
        if ' ' in query:
            self.doubleWord(query)
        elif query.strip(): # checks if the string is not empty!
            self.singleWord(query)
        else:
            print "Nothing Entered!"

if __name__ == '__main__':
    srch = Search()
    query = raw_input("Enter the query: ")
    start = time.time()
    srch.returnRes(query)
    end = time.time()
    print "The time taken for the result is: ", end-start, " secs"
