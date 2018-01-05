import re
import zlib
import subprocess as sp
wikiFile = 'output.dat'

def parse():
    # |$ to get just the first match.
    regex = ['<title>(.*?)</title>', '<id>(.*?)</id>|$', '<text xml:space="preserve">(.*?)</text>']  # tags to parse
    wiki = open(wikiFile, 'r')
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
    print "Title: ", pTitle.group(1)
    print "ID: ", pID.group(1)
    print zlib.decompress(pText.group(1))

if __name__ == '__main__':
    parse()