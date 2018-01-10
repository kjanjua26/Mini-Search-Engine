import pickle
from collections import defaultdict
import time

pickleFile = "dumpedDict.pickle"
tempList = []

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
            tempList.append([x for x in docs.split(';')])
        except:
            print("\nThe term isn't in the docs!")
        print("The word is in: ", tempList)  # gets the docs.

    def combine(self, list):
        return set().union(*list) # gets the union of all the lists.

    def doubleWord(self, query):
        dList = [] # temporary list.
        query = query.split(' ')
        for term in query:
            docs = self.search(term)
            try:
                dList.append([x for x in docs.split(';')]) #gets the docs.
            except:
                print("The word that isn't in the docs is: ", term)
        print("The words in the docs are: ", ', '.join(self.combine(dList)))

    def returnRes(self, query):
        query = query.lower()
        if ' ' in query:
            self.doubleWord(query)
        elif query.strip(): # checks if the string is not empty!
            self.singleWord(query)
        else:
            print("Nothing Entered!")

if __name__ == '__main__':
    srch = Search()
    query = input("Enter the query: ")
    start = time.time()
    srch.returnRes(query)
    end = time.time()
    print("The time taken for the result is: ", end-start, " secs")
