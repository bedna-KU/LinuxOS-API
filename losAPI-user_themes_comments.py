#!/usr/bin/env python3
import urllib3
import dhtmlparser as d
from bs4 import BeautifulSoup
import argparse
import time
import sys
import os

# Set input args
ap = argparse.ArgumentParser ()
ap.add_argument ("-u", "--user_id", type = str, required = True,
	help = "user_id")
args = vars (ap.parse_args ())

# User ID
user_id = args["user_id"]

server_path = "https://linuxos.sk"
link_base_path = "https://linuxos.sk/profil/13656/prispevky/komentare/"

def parser (data):
	orig_stdout = sys.stdout
	sys.stdout = open('trash', 'w')
	dom = d.parseString (r.data.decode ("utf-8"))
	sys.stdout = orig_stdout
	return dom

http = urllib3.PoolManager ()
r = http.request ("GET", link_base_path)

print ("x      xxxxx  xxxxx           x    xxxx     x  ")
print ("x      x   x  x              x x   x   x    x  ")
print ("x      x   x  xxxxx  xxxxx  x   x  xxxx     x  ")
print ("x      x   x      x         xxxxx  x        x  ")
print ("xxxxx  xxxxx  xxxxx         x   x  x        x  ")


if r.status == 200:
	dom = parser(r.data.decode ("utf-8"))
	# Get the number of pages
	pagination = dom.find ("li", {"class": "page "})
	a_tag = BeautifulSoup (str (pagination[3]), "html.parser").find('a')
	count_pages = int (a_tag.text)

	# Get main pages with comments
	links = []
	for i in range (1, count_pages + 1):
		# print (link_base_path + str (i) + "/")
		r = http.request ("GET", link_base_path + str (i) + "/")
		if r.status == 200:
			dom = parser(r.data.decode ("utf-8"))
			# Get links from page
			links_in_td = dom.find ("td", {"class": "title"})
			for link_line in links_in_td:
				a_tag = BeautifulSoup (str (link_line), "html.parser").find('a', href=True)
				print (a_tag["href"])
				links.append (a_tag["href"])

		time.sleep (1)

	print ("***************************")
	print ("*** Write links to file ***")
	print ("***************************")
	with open ("user_themes_comments.txt", "w") as f:
		for listitem in links:
		    f.write ('%s\n' % listitem)

else:
	print ("Do not open url")