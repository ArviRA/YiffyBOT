import requests
from bs4 import BeautifulSoup
print("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format('Iron'))
all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format('Iron'))
page = BeautifulSoup(all_links.content, 'html.parser')
mydivs = page.findAll("a", {"class":"browse-movie-title"})
search_result = []
for i in mydivs:
    dummy=i.text
    if "[" in dummy :
        dummy = dummy.split("] ")[1]
   
    search_result.append(dummy)
print(search_result)
movie = requests.get("https://yts.mx/movies/{}".format(search_result[1]))