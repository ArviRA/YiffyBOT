import requests
from bs4 import BeautifulSoup
print("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format('Iron'))
all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format('Iron'))
page = BeautifulSoup(all_links.content, 'html.parser')
mydivs = page.findAll("a", {"class":"browse-movie-title"})
for i in mydivs:
    dummy=i.text
    print(dummy)