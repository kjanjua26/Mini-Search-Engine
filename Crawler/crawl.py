import requests
from bs4 import BeautifulSoup
import csv


#does basic crawling, gets the raw text.

def getData(link):
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	parser_tag = soup.find_all('div', attrs={'class':'mw-parser-output'}) #gets tags from class: mw-parser-output
	for i in parser_tag:
		print i.text #prints the text from the tags returned from class: mw-parser-output

if __name__ == '__main__':
	keyword = "Nelson_Mandela"
	link = "https://simple.wikipedia.org/wiki/{}".format(keyword)
	getData(link)
