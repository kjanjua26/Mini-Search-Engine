import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import zlib

class Parse:
    count = 0
    articleList = defaultdict(list)

    def __init__(self):
        pass

    def fileNames(self):
        self.outputFile = "ouput.dat"

    def writeFile(self, text):
        file = open(self.outputFile, 'w')
        file.write("<parseRoot>") # first root.

        file.write("</parseRoot>")
        file.close()

    def getData(self, url):  # does basic crawling, gets the raw text.
        self.fileNames()
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        parser_tag = soup.find_all('div', attrs={'class': 'mw-parser-output'})  # gets tags from class: mw-parser-output
        self.count += 1
        for i in parser_tag:
            self.articleList[self.count] = i.text.encode('utf-8')

    def compressData(self): #compressing the text in the hashtable.
        for key in self.articleList.iterkeys():
            self.articleList[key] = zlib.compress(self.articleList[key])

if __name__ == '__main__':
    instance = Parse() #creating object of class.
    keyword = ['Nelson Mandela', 'Cricket']
    for i in keyword:
        url = "https://simple.wikipedia.org/wiki/{}".format(i)
        instance.getData(url)
    instance.compressData()
    print instance.articleList
