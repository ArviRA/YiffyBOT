import requests
from bs4 import BeautifulSoup
import re
import json
search_result = []
all_links = requests.get("https://yifytorrent.vip/search?keyword=avengers")
page = BeautifulSoup(all_links.content, 'html.parser')
divs=page.find("div",{"class":"homepage-dt"})
for link in divs.find_all("a"):
   if link.text != '\n\n \n': 	
   	#print(len(link.text),link['href'])
   	test = link['href'].split("-")	
   	test[0] = ''.join([i for i in test[0] if not i.isdigit()]).replace("movie","movies")
   	test = "-".join(test).replace("-","",1)
   	#print(test) 
   	search_result.append((link.text,test))
print(search_result)

print("base","https://www.yst.am{}".format(search_result[0][1]))
all_links = requests.get("https://www.yst.am{}".format(search_result[0][1]))
page = BeautifulSoup(all_links.content, 'html.parser')
years=page.find("div",{"id":"movie-info"})
years=str(years)[0:150]
id = re.search('("\d+")',years).group().strip('"')   
print("\n\n\n\n id:::::",id)
movie=requests.get("https://yts.mx/api/v2/movie_details.json?movie_id={}".format(id))
movie = json.loads(movie.content)
image_url=movie["data"]["movie"]['large_cover_image']
rating =str(movie["data"]["movie"]['rating']) + " \U0001F31F"
run_time = str(movie["data"]["movie"]['runtime'])+" minutes \U0001F554"
genre = movie["data"]["movie"]['genres']
certificate = str(movie["data"]["movie"]['mpa_rating']) + "\U0001F4A9"
            #print(rating ,run_time," ",genre," ",certificate)
quality = []
quality = movie["data"]["movie"]['torrents']
torrents = []
for i in range(len(quality)):
     qua = str(quality[i]["quality"])+"\U0001F4C0"
     url = quality[i]["url"]
     size = str(quality[i]["size"])+"\U0001F4C2"
     torrents.append((qua,size,url))

print(rating,run_time,genre,certificate)
print(torrents)  

print(search_result[0][0])
if "Avengers: Endgame (2019)" == search_result[0][0] :
	print("fail")

