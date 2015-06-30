import praw, re, requests, imdbparser, time
from bs4 import BeautifulSoup, SoupStrainer 

r = praw.Reddit(user_agent = 'IMDb parser by Dephinite')
r.login('imdbbot2', 'enter-password-here', disable_warning = True)
already = []
sp = ', '

def comment_reply(movie):
	comm = ("**Movie Details:** \n \n")
	comm += ('**Title:** ' + movie['title'] + '\n \n')
	comm += ('**IMDb Rating:** ' + movie['rating'] + '\n \n')
	comm += ('**Director(s):** ' + sp.join(movie['director']) + '\n \n')
	comm += ('**Writer(s):** ' + sp.join(movie['writer']) + '\n \n')
	comm += ('**Genre(s):** ' + sp.join(movie['genres']) + '\n \n')
	comm += ('**Runtime(s):** ' + sp.join(movie['duration']) + '\n \n')
	comm += ('**Description:** ' + movie['description'] + '\n \n')
	comm += ("--- \n \n  ^This ^is ^a ^bot ^post. ^Message ^for ^suggestions/feedback." )

	return comm

def run_bot():
	sub = r.get_subreddit('test')
	comments = sub.get_comments(limit = 50)
	for comment in comments:
		flag = re.search('a href="http://www.imdb.com/title/.*/"', comment.body_html)
		if comment.id not in already and flag:
			links = BeautifulSoup(comment.body_html, parse_only = SoupStrainer('a', href = re.compile('http://www.imdb.com/title/')))

			for link in links:
				comment.reply(comment_reply(imdbparser.parse(requests.get(link['href']).text)))
				already.append(comment.id)


while(True):
	run_bot()
	print('Sleeping...')
	time.sleep(10)


