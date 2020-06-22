#!/usr/bin/env python3
import urllib3
import dhtmlparser as d
from bs4 import BeautifulSoup
import argparse
import time
import sys
import os
import re
import json

# Set input args
ap = argparse.ArgumentParser ()
ap.add_argument ("-u", "--user_id", type = str, required = True,
	help = "user_id")
args = vars (ap.parse_args ())

# User ID
user_id = args["user_id"]

server_path = "https://linuxos.sk"

# Muted parse
def parser (data):
	orig_stdout = sys.stdout
	sys.stdout = open('trash', 'w')
	dom = d.parseString (r.data.decode ("utf-8"))
	sys.stdout = orig_stdout
	return dom

print ("")
print ("x      xxxxx  xxxxx           x    xxxx     x  ")
print ("x      x   x  x              x x   x   x    x  ")
print ("x      x   x  xxxxx  xxxxx  x   x  xxxx     x  ")
print ("x      x   x      x         xxxxx  x        x  ")
print ("xxxxx  xxxxx  xxxxx         x   x  x        x  ")
print ("")

links = []
# Read links
with open ("user_themes_comments.txt", "r") as f:
	for line in f:
		line = line[:-1]
		links.append (line)

for link in links:
	absolute_path = (server_path + link)
	# Get page
	http = urllib3.PoolManager ()
	r = http.request ("GET", absolute_path)

	if r.status == 200:
		dom = parser (r.data.decode ("utf-8"))
		# Get all comments
		comments_dirty = dom.find ("div", {"class": "comment-container"})
		user_name = [None] * len (comments_dirty)
		user_link = [None] * len (comments_dirty)
		comments_text = [None] * len (comments_dirty)
		comments_id = [None] * len (comments_dirty)
		comments_parent = [None] * len (comments_dirty)
		for number in range(1, len (comments_dirty)):
			comments_dirty[number] = str (comments_dirty[number])
			parent = BeautifulSoup (str (comments_dirty[number]), "html.parser").select ('a[class="parent-link"]')
			if parent:
				comments_parent[number] = parent[0]["href"]
			comment_id = BeautifulSoup (str (comments_dirty[number]), "html.parser").select ('a[class="headerlink"]')
			if comment_id:
				comments_id[number] = comment_id[0]["href"]
			user_span = BeautifulSoup (str (comments_dirty[number]), "html.parser").select ('span[class="user_link"]')
			comment_dirty_text = BeautifulSoup (comments_dirty[number], "html.parser").select ('div[class="text"]')
			if comment_dirty_text:
				comment_dirty_text = BeautifulSoup (str (comment_dirty_text[0]), "html.parser")
				# Remove blockquote
				for bq in comment_dirty_text.select ("blockquote"):
					bq.decompose ()
				# Extract only text
				comment_clean_text = comment_dirty_text.text
				# Remove new lines
				comment_clean_text = re.sub ("\n+", " ", comment_clean_text)
				# Trim string
				comment_clean_text = comment_clean_text.strip ()
				comments_text[number] = comment_clean_text
				user_name[number] = user_span[0].text
				user_href = BeautifulSoup (str (user_span), "html.parser").find ('a')
				if user_href:
					user_link[number] = user_href["href"]

	for number in range (len (user_link)):
		if "/profil/" + str (user_id) +  "/" == user_link[number]:
			print ("============================================")
			if comments_parent[number]:
				for i in range (len (comments_id)):
					if comments_id[i] == comments_parent[number]:
						print ("PARENT :", comments_text[i])
						print ("COMMENT:", comments_text[number])
						with open ('comments_parent.txt', 'a') as file:
							file.write (comments_text[i] + "\n")

						with open ('comments_user.txt', 'a') as file:
							file.write (comments_text[number] + "\n")

	time.sleep (1)