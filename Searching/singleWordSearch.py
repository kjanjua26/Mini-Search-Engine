import pickle
from collections import defaultdict

pickleFile = "pFile.pickle"


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

    def returnResult(self, query):
        docs = self.search(query)
        if ' ' in query: # Multiword, faster than len(query.split()) > 1
            print "Multi!"
        else:
            if(len(docs) == 1):
                print 'Not in the document!'
            else:
                print 'The word is in document: ', [x[0] for x in docs.split(';')] # gets the docs.

if __name__ == '__main__':
    srch = Search()
    query = raw_input("Enter the query: ")
    srch.returnResult(query)
    print srch.hitList
