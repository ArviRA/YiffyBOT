import requests
from bs4 import BeautifulSoup
import re
import json


link=requests.get("https://www.yst.am/movies/se7en-1995")
print(link.content)