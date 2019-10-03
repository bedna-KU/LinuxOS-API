#!/usr/bin/env python3

# Get users without posts (save to file "Users_without_posts")

import time
import requests
from bs4 import BeautifulSoup

for user_number in range (1, 47888):
	url = "http://linuxos.sk/profil/{}/prispevky/".format(user_number)
	print (url)
	r = requests.get (url, allow_redirects=True)
	if r.status_code == 200:
		html = r.content
		parsed_html = BeautifulSoup (html, "lxml")
		content = parsed_html.body.find ('div', attrs = {'class':'module-row'})
		user = parsed_html.body.find ('a', attrs = {'href':'/profil/' + str (user_number) + '/'})
		print ("USER:", user.text)

		sub_contents = content.select ('a')
		if sub_contents:
			for sub_content in sub_contents:
				print (sub_content.text)
		else:
			print ("User has no posts")
			# ~ print ("---", str (user.text))
			open ("Users_without_posts", "a").write (user.text + "   " + str (user_number) + "\n")
	else:
		print ("User does not exist")
		
	time.sleep (1)
