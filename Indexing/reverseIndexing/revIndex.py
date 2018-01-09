import re
from collections import defaultdict
from array import array
from bs4 import BeautifulSoup as BS
import csv
from tqdm import tqdm

hitList = defaultdict(list)
textList = []
titles = []
ids = []
pickleTable = defaultdict(list)

class HashTable:
	def __init__(self, source, grammerFile, output):
		self.filename = source
		self.csvFile = output
		gFile = open(grammerFile, 'r')
		self.grammerDoc = [line.strip() for line in gFile]  # gets the list of the grammerFile we want to clear, strips the '\n'

	def writeFile(self):
		print('\n\nWriting...')
		myFile = open(self.csvFile, 'w')

		#for key in hitList.iterkeys(): # python 2.7
		for key in tqdm(hitList.keys()): # python 3.x
			temp = []
			for val in hitList[key]:
				docID = val[0]
				occurence = val[1]
				temp.append(':'.join([docID, ','.join(map(str,occurence))]))
			inStr = ';'.join(temp)
			myFile.write(key+","+str(inStr)+"\n")
			key = key.lower() # lower to make searching easier
			pickleTable[key] = inStr
		myFile.close()
		
	def getKeys(self, textLine):
		line = re.sub('[^0-9a-zA-Z]+', ' ', textLine) #replaces the non-ASCII values with space
		line = line.split()
		line = [x for x in line if x not in self.grammerDoc]  # eliminate the articles, prepositions etc.
		return line

	def parse(self):
		wiki = open(self.filename, 'r', encoding="UTF-8")
		pageList = []
		print('Reading the corpus...');
		for line in tqdm(wiki):
			pageList.append(line.strip().lower()) # oomparisons are case sensitive so make all lower

		soup = BS(' '.join(pageList), 'html.parser')

		print('\nParsing IDs...')
		for i in tqdm(soup.select('page > id')):
			ids.append(i.text)

		print('\nParsing Titles...')
		for i in tqdm(soup.findAll('title')):
			titles.append(i.text)
		
		print('\nParsing Text...')
		for i in tqdm(soup.findAll('text')):
			textList.append(i.text)

	def createhashtable(self):
		self.parse()
		print('\n\nIndexing...')
		for i in tqdm(range(len(textList))):
			invertedIndex = {}
			keys = self.getKeys(titles[i])
			for key in keys:
				try:
					invertedIndex[key][1].append(0)
				except:
					invertedIndex[key] = [ids[i], array('L', [0])]  # L for unsigned Long -> 4 Bytes, hashtable[id, [ArrayList]]

			keys = self.getKeys(textList[i])
			for value, key in enumerate(keys):
				try:
					invertedIndex[key][1].append(value+1)
				except:
					invertedIndex[key] = [ids[i], array('L', [value+1])]  # L for unsigned Long -> 4 Bytes, hashtable[id, [ArrayList]]

			#for curPage, invPag in invertedIndex.iteritems(): #python 2.7
			for curPage, invPag in invertedIndex.items(): #python 3.x
				hitList[curPage].append(invPag)  # updates the defaultdict with each new page.
		self.writeFile()
	
	def pickling(self): # Serializes the hashtable to be read for the searching part.
		pickleFile = open("self.dumpedDict.pickle", "wb") #opening the pickle file to write the byte stream.
		pickle.dump(pickleTable, pickleFile)
		pickleFile.close()

if __name__ == "__main__":
	invIndex = HashTable("sample.dat", "grammer.rtf", "sampleData.csv", "dumpedDict.pickle")
	invIndex.createhashtable()
	invIndex.pickling()
