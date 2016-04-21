# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import random

def get_soup_object(url):
	source_code = requests.get(url)
	if source_code.status_code == 404:
		return None
	source_code = source_code.text

	soup = BeautifulSoup(source_code)

	return soup

def visit_pages_to_extract(url, category):
	dfile = open("data/"+category[1:],'w')
	soup = get_soup_object(url+category)

	for body in soup.findAll('div',{'itemprop':'articleBody'}):
		text = ""
		for article in body.findAll('div', recursive=False):
			if article.text.strip() != text.strip():
				text = article.text.strip()
				print text
			color = ""
			for propertyDiv in article.findAll('div'):
				try:
					style = propertyDiv['style']
					index = style.find(' color:')
					if index != -1 and style[index+7] != ';':
						color = style[index+7:index+14]
						print color
				except:
					pass
					#print "No color found"
			if color == "":
				print "Inside color"
				value = random.randint(0,15777215)
				value = hex(value)
				value = '#' + value[2:]
				print value
				color = value

			final_text = "<font color='"+ color +"' >"+ text + "</font>"
			final_text = unicode(final_text)
			final_text = final_text.encode('utf-8')
			final_text.replace('\n', " ")
			dfile.write("$#\n")
			dfile.write(final_text + "\n")
		
	dfile.close()

def catch_all_links(url):
	category_array = []
	soup = get_soup_object(url)
	for category in soup.findAll('div',{'id':'botlist'}):
		for link in category.findAll('a',href=True):
			text = link['href']
			category_array.append(text)
	return category_array


if __name__ == '__main__':
	url = "http://www.factslides.com"
	links = catch_all_links(url)
	for link in links:
		visit_pages_to_extract(url, link)