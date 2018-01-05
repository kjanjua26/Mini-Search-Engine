import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import zlib # to compress.

class Parse:
    keyword = ['Nelson Mandela', 'Cricket']
    count = 0
    articleList = defaultdict(list)

    def __init__(self):
        pass

    def fileNames(self):
        self.outputFile = "output.dat"

    def writeFile(self):
        file = open(self.outputFile, 'w')
        file.write("<parseRoot>\n")  # first root.
        for key in self.articleList:
            file.write("<page>\n")
            file.write("<id>{}</id>\n".format(key))
            file.write("<title>{}</title>\n".format(self.keyword[key-1]))
            file.write('<text xml:space="preserve">')
            file.write(self.articleList[key])
            file.write("</text>")
            file.write("</page>\n")
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

    def compressData(self): # compressing the text in the hashtable.
        for key in self.articleList.iterkeys():
            self.articleList[key] = zlib.compress(self.articleList[key])

if __name__ == '__main__':
    instance = Parse() #creating object of class.
    for i in instance.keyword:
        url = "https://simple.wikipedia.org/wiki/{}".format(i)
        instance.getData(url)
    instance.compressData()
    instance.writeFile()
