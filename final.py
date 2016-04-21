# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup

base_url = 'http://www.santabanta.com'

visited_url_list = []

def get_soup_object(page_url, page):
	url = base_url + page_url +'/?page='+str(page)
	source_code = requests.get(url)
	if source_code.status_code == 404:
		return None
	source_code = source_code.text

	soup = BeautifulSoup(source_code)

	return soup

def visit_pages(page_url, max_pages, filename):
	page = 1
	store = open(filename,'w')

	soup = get_soup_object(page_url,1)

	while page <= max_pages:
		url = base_url + page_url +'/?page='+str(page)
		soup = get_soup_object(page_url, page)
		if soup == None:
			break
		
		joke_count = 0
		for joke in soup.findAll('div',{'class':'sms_list_box_1'}):
			for title in joke.find('a'):
				title = unicode(title.string)
				title = title.encode('utf-8')
				title = title.replace('None','.')
				title = title.replace('\n','.')
				title = title.replace('\n','.\n')
				#print title
				store.write("$\n"+title+"\n")

			for body in joke.find('td'):
				body = unicode(body.string)
				body =  body.encode('utf-8')
				body = body.replace('None','.')
				body = body.replace('\n','.\n')
				store.write(body+"\n")
			store.write("@#\n")
			joke_count += 1
		store.flush()
		print "Url "+url+" downloaded"
		page += 1
		if joke_count == 0:
			print "XXXXXXXXXXX Breaking Out XXXXXXXXXXX"
			store.close()

	store.close()

def find_other_links(mySoup):
	for link in mySoup.findAll('a'):
		href = link.get('href')
		if not href in visited_url_list:
			print "HREF: ",href
			if href.startswith('http'):
				visited_url_list.append(href)
				continue
			visit_pages(href,100, href.split('/')[-2]+'.txt')

if __name__ == '__main__':
	rel_url = '/jokes/hindi-jokes'
	visit_pages(rel_url, 312, "hindi_veg.txt")
	