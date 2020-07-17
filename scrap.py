import requests

all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format("se7en"))
print(all_links)