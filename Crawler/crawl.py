import requests
from bs4 import BeautifulSoup
import csv

def getData(link):
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	parser_tag = soup.find_all('div', attrs={'class':'mw-parser-output'})
	for i in parser_tag:
		print i.text

if __name__ == '__main__':
	keyword = "Nelson_Mandela"
	link = "https://simple.wikipedia.org/wiki/{}".format(keyword)
	getData(link)
