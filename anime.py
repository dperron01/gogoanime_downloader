from lxml import html
import requests
import urllib.request
from time import sleep
import sys

animes = input("Anime: ")
animes = animes.split()

url = "https://ww4.gogoanime.io//search.html?keyword="

for anime in animes:
	url = url + anime + "%20"

page = requests.get(url)
tree = html.fromstring(page.content)
#This will create a list of buyers:
urls = tree.xpath('//div[@class="last_episodes"]/ul[@class="items"]/li/p[@class="name"]/a/@href')
names = tree.xpath('//div[@class="last_episodes"]/ul[@class="items"]/li/p[@class="name"]/a/@title')

print("Animes found matching that selection:")
count = 0
for name in names:
	print(count, ": ", name)
	count += 1

selection = input("Selection: ")
s = int(selection)

title = names[s]

url = "https://ww4.gogoanime.io" + urls[s]
print(url)
page = requests.get(url)
tree = html.fromstring(page.content)
lastep = tree.xpath('//a[@class="active"]/@ep_end')[0]
print("Found ", lastep, " episodes!")

print("Which episodes do you want to download?")
start = int(input("Starting Episode: "))
end = int(input("Ending Episode: "))


epurls = []
for i in range(start, end+1):
	location = "-".join(title.lower().split())
	location = "https://ww4.gogoanime.io/" + location + "-episode-" + str(i)
	epurls.append(location)

#file = open("urls.txt", "w")

#print(epurls)
counter = start
for epurl in epurls:
	page = requests.get(epurl)
	tree = html.fromstring(page.content)
	dl = tree.xpath('//div[@class="download-anime"]/a/@href')
	dlpage = requests.get(dl[0])
	dltree = html.fromstring(dlpage.content)
	magic = dltree.xpath('//div[@class="mirror_link"]/div/a/@href')
	print("Downloading episode ",str(counter))
	try:
		urllib.request.urlretrieve(magic[0], "_".join((title+" episode " + str(counter) + ".mp4").split()))
	except: 
		print("Download failed!")
		print("Try these links:")
		for m in magic:
			print(m)

		# print("trying openload")
		# dlnames = dltree.xpath('//div[@class="mirror_link"]/div/a/text()')
		# index = 0
		# found = False
		# for dname in dlnames:
		# 	print(dname)
			# if dname == "Download Openload":
			# 	found = True
			# 	print("Openload present")
			# 	break
			# index += 1
		# if found:
		# 	opage = dlpage = requests.get(magic[index])
		# 	otree = html.fromstring(opage.content)
		# 	sid = otree.xpath('//span/text()')
		# 	print(sid)
		# 	urllib.request.urlretrieve(magic[index], "temp.txt")

		# 	ourl = "https://oload.stream/stream/" + str(sid)
			#print(ourl)
			#urllib.request.urlretrieve(ourl, "_".join((title+" episode " + str(counter) + ".mp4").split()))



	# print("Downloading episode ",str(counter))
	# print("Waiting to download the next one")
	#file.write(magic[0] + "\n")
	counter += 1

