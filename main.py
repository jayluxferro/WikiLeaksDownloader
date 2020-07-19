#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import subprocess
import threading
import sys
from time import sleep

# default definitions
base_url = "https://wikileaks.org/vault7/document/"

def download_file(target_url, filname):
	print("[+] Downloading: " + str(file_name))
        subprocess.call(['wget', target_url, '-O', file_name])

def searchForDownloadLinks(link):
	folder_name = link[12:]
	download_page = urllib2.urlopen(base_url + link)
	page_content = "".join(download_page.readlines())
	download_links = BeautifulSoup(page_content, "lxml")
	for dl in download_links.find_all('a'):
		download_link = dl.get('href')
		dl = str(download_link)
		if dl[len(dl)-3:len(dl)] == "pdf":
			download_urls.append(base_url + link + download_link)
			print("[+] Download link found: " + str(dl))

# getting web page
web_data = urllib2.urlopen(base_url)
web_data = "".join(web_data.readlines())

# retrieving links
download_urls = []
all_links = []
counter = 0
links = BeautifulSoup(web_data, "lxml")
for link in links.find_all('a'):
	current_link = link.get('href')
	# performing match
	if str(current_link[3:11]) == "document":
		if counter == 0:
			pass
		else:
			all_links.append(current_link)
			print("[+] Link found: " + str(current_link))
		counter += 1

threads = []

for link in all_links:
    t = threading.Thread(target=searchForDownloadLinks, args=(link,))
    threads.append(t)

# Start all threads
for x in threads:
    sleep(.1)
    x.start()

 # Wait for all of them to finish
for x in threads:
    x.join()


for x in range(len(download_urls)):
	file_name = str(download_urls[x]).split("/")[-1]
        download_file(download_urls[x], file_name)
