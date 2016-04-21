import requests
from bs4 import BeautifulSoup

base_url = 'http://www.santabanta.com'

def visit_pages(page_url, max_pages, filename):
	page = 1
	store = open(filename,'w')
	while page <= max_pages:
		url = base_url + page_url +'/?page='+str(page)
		source_code = requests.get(url)
		if source_code.status_code == 404:
			break
		source_code = source_code.text

		soup = BeautifulSoup(source_code)
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
	store.close()

if __name__ == '__main__':
	rel_url = '/jokes/restricted-hindi-jokes'
	visit_pages(rel_url, "hindi_non_veg.txt")

	rel_url = '/jokes/hindi-jokes/hindi/411'
	visit_pages(rel_url, "santa_banta.txt")