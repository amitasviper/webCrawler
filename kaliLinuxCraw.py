# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup

def get_soup_object():
	url = "http://theporndude.com/"
	source_code = requests.get(url)
	if source_code.status_code == 404:
		return None
	source_code = source_code.text

	soup = BeautifulSoup(source_code)

	return soup

def visit_pages(filename):
	store = open(filename,'w')

	soup = get_soup_object()
		

	for link in soup.findAll('a',{'class':'link'}, href=True):
		text = link['href']
		text = text.replace('http://','')
		text = text.replace('https://','')

		if text[-1] == '/':
			text = text[0:-1]

		if text[0:4] == 'www.':
			store.write('127.0.0.1 '+text+'\n')
			text = text[4:]
			store.write('127.0.0.1 '+text+'\n')
		else:
			store.write('127.0.0.1 '+text+'\n')
			text = 'www.' + text
			store.write('127.0.0.1 '+text+'\n')

		print text
	store.flush()

	store.close()


if __name__ == '__main__':
	visit_pages("pornList.txt")