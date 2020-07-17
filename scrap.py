import requests
from bs4 import BeautifulSoup

all_links = requests.get("https://yts.ws/movie/se7en-1995")
page = BeautifulSoup(all_links.content, 'html.parser')
years=page.find("div",{"class":"ava11"})
print(type(years))
print(years.find_all(href=True))
