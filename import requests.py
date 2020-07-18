import requests
from bs4 import BeautifulSoup
import re
import json


link=requests.get("https://www.yst.am/movies/the-iron-mask-2019")
link=BeautifulSoup(link.content,"html.parser")
print(link.prettify)