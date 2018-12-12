from bs4 import BeautifulSoup

import requests, json

page = 1

art_list = []

while page <= 26:

	url = "https://www.tate.org.uk/search?aid=558&type=artwork&wot=6&page=" + str(page) + "&ajax=1&ajax_scope=card-group" 
	page = page + 1
	print(url)

#print("Scraping!",url)

	collection_page = requests.get(url)
	page_html = collection_page.text

	soup = BeautifulSoup(page_html, "html.parser")

	print(page_html)
	print(soup.prettify())



	#urls = soup.find('a', {'data-gtm-name' :'card_link_artist'})
	#urls= soup.find('a')
	
	cards = soup.find_all('div', {'class': 'card'})
	for card in cards:
		a_turner = {}
		print('__________')
		# print(card)

		# card = soup.find('div', {'class': 'card'})
		# print('__________')
		# print(card)

		artist_name = card.find('a', {'data-gtm-name' :'card_link_artist'})
		# print(artist_name)
		if artist_name is None:
			a_turner["artist_name"] = "no title"
		else:
			a_turner["artists"] = artist_name.text

		date = card.find('span', {'class' :'card__when--artwork-date'})
		# print(date)
		a_turner["date"] = date.text.replace(u'\u2013',u'')

		titles = card.find('a', {'data-gtm-name' :'card_link_title'})
		# print(titles)
		a_turner["titles"] = titles.get_text(strip=True).replace(u'\u2019',u'') 
		# print(titles)
		#pull ['href'] from titles:
		url = "https://www.tate.org.uk" + titles['href']
		print("scraping" , url)
		description_page = requests.get(url)
		page1_html = description_page.text
		artsoup = BeautifulSoup(page1_html, "html.parser")
		# print(page1_html)

		description = artsoup.find('div', {'class': 'artwork__text'})
		if description is None:
			a_turner["description"] = "no description"
		else: 
			a_turner["description"] = description.get_text(strip=True).replace(u'\u2013',u'').replace(u'\u2019',u'').replace(u'\u2018',u'').replace(u'\u2026',u'')

	

		divTag = artsoup.find("dl", {"class": "tombstone"})
		# for tag1 in divTag:
		dtTags = divTag.find_all("dt", {'class':'tombstone__title'})
		# print(dtTags)

		# 	a_turner["dtTags"] = tag1.text
		for tag in dtTags:
			print(tag, tag.next_sibling)
			a_turner[tag.get_text(strip=True).replace(u'\u2013',u'')] = tag.next_sibling.get_text(strip=True).replace(u'\u2013',u'')
		

		print(a_turner)
		art_list.append(a_turner)


print(art_list)
page = page + 1
json.dump(art_list,open('art_list.json','w'),indent=2)
	

