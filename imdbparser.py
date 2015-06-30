import requests, re, sys
from bs4 import BeautifulSoup 



data = requests.get('http://www.imdb.com/title/tt0068646/').text #Placeholder value


def parse(data):
	mov = {}
	soup = BeautifulSoup(data)

	links = soup.find_all('h1', class_ = "header")
	for link in links:
		mov['title'] = link.contents[1].string


	classname = "titlePageSprite star-box-giga-star"
	links = soup.find_all('div', class_ = classname)
	for link in links:
		mov['rating'] = link.contents[0].string


	mov['genres'] = []
	links = soup.find_all('span', class_ = "itemprop", itemprop = "genre")
	try:
		for link in links:
			mov['genres'].append(link.string)
	except IndexError:
		mov['genres'] = 'Not Specified'


	links = soup.find_all('p', itemprop = "description")
	try:
		for link in links:
			mov['description'] = link.string
	except IndexError:
		mov['description'] = 'Not Specified'


	mov['duration'] = []
	links = soup.find_all('time', itemprop = "duration")
	try:
		for link in links[1:]:
			mov['duration'].append(link.string)
	except IndexError:
		mov['duration'] = 'Not Specified'


	mov['director'] = []
	links = soup.find_all('h4', class_ = 'inline', text = ['Director:', 'Directors:'])
	for link in links[0].next_siblings:
		try:
			mov['director'].append(link.contents[0].contents[0])
		except:
			fubar = 1


	mov['writer'] = []
	links = soup.find_all('h4', class_ = 'inline', text = ['Writer:', 'Writers:'])
	for link in links[0].next_siblings:
		try:
			mov['writer'].append(link.contents[0].contents[0])
		except AttributeError:
			fubar = 1    #Placeholder statement inside except block.

	return mov
