import requests
from bs4 import BeautifulSoup
import telebot
import re
import json
import os
from telebot import types
from flask import Flask, request

TOKEN = '1010311458:AAFiDsa4J4pYXAi8UOblX2Vo3D7V8RhuvHg'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

user = {}

def sendMessage(message, text):
   bot.send_message(message.chat.id, text)
# This method will send a message formatted in HTML to the user whenever it starts the bot with the /start command, feel free to add as many commands' handlers as you want
@bot.message_handler(commands=['start'])
def send_info(message):
   text = (
   "<b>Welcome to the Yify BOt 🤖!</b>\n"
   "Say /help to the bot to get to know about it!"
   )
   print("\n\n\n:message",message)
   bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_info(message):
   text = (
   "<b>Welcome to the Yify BOt 🤖!</b>\n"
   "use /start to start the bot \n"
   "use /search for searching movies\n "
   "Then select the movies from the list\n"
   "use /back to go back to thee list \n"
   "select the Quality of movie\n download the torrent! have fun."
   )
   bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['search'])
def send_info(message):
   global user
   text = (
   "Enter the movie name to search"
   )
   user[str(message.from_user.id)]={"search" : True,"select":False,"quality":False,"search_result":[],"torrents":[]}
   print("\n\n\n",user)
   bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['back'])
def send_info(message):
   user[str(message.from_user.id)]["search"] = False
   user[str(message.from_user.id)]["select"] = True
   user[str(message.from_user.id)]["quality"] = False
   if len(user[str(message.from_user.id)]["search_result"]) !=0 : 
    for i in user[str(message.from_user.id)]["search_result"]:
                keyword = str(i[0])
                item = types.KeyboardButton(keyword)
                markup.add(item)
    user[str(message.from_user.id)]["search_result"] = search_result
    bot.send_message(current_message.from_user.id, "Choose a movie:", reply_markup=markup)
   else:
      bot.send_message(current_message.from_user.id, "No searches found!!!")

@bot.message_handler(commands=['exit'])
def send_info(message):
   global user
   user.pop(str(message.from_user.id))
# This method will fire whenever the bot receives a message from a user, it will check that there is actually a not empty string in it and, in this case, it will check if there is the 'hello' word in it, if so it will reply with the message we defined
@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
   global user
   if 'hello'in message.text.lower():
      sendMessage(message, 'Hello! How are you doing today?')
   else:
      print(user[str(message.from_user.id)]["search"],"the trialll")
      if(user[str(message.from_user.id)]["search"]):
        base_url = ""
        
        #if back == False:
        current_message = message
        print("\n\n\n message ",message.text,"\n\n\n")
        #all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format(message.text))
        #print(all_links)
        #page = BeautifulSoup(all_links.content, 'html.parser')
        #mydivs = page.findAll("a", {"class":"browse-movie-title"},href=True, text=True)
        #years=page.findAll("div",{"class":"browse-movie-year"})
        #print("\n\n\n\nMy div",mydivs,"\n\n\n\n")
        #search_result = []
        #for i,j in zip(mydivs,years):
        #    dummy=i.text
        #    if "[" in dummy :
        #        dummy = dummy.split("] ")[1] 
    
        #    search_result.append((dummy,j.text,i["href"]))
        search_result = []
        all_links = requests.get("https://yifytorrent.vip/search?keyword={}".format(message.text))
        page = BeautifulSoup(all_links.content, 'html.parser')
        divs=page.find("div",{"class":"homepage-dt"})
        for link in divs.find_all("a"):
          if link.text != '\n\n \n':
            test = link['href'].split("-")  
            test[0] = ''.join([i for i in test[0] if not i.isdigit()]).replace("movie","movies")
            test = "-".join(test).replace("-","",1) 
            search_result.append((link.text,test))
        print("\n\n\n\n search result",search_result)
        markup = types.ReplyKeyboardMarkup(row_width=4)
        #print(search_result)
        if len(search_result) != 0:
            user[str(message.from_user.id)]["search"] = False
            user[str(message.from_user.id)]["select"] = True
            for i in search_result:
                keyword = str(i[0])
                item = types.KeyboardButton(keyword)
                markup.add(item)
            user[str(message.from_user.id)]["search_result"] = search_result
            bot.send_message(current_message.from_user.id, "Choose a movie:", reply_markup=markup)
        else :
            bot.reply_to(current_message, current_message.from_user.first_name + ",No such movies are present! try again\n /search")   
      
      elif user[str(message.from_user.id)]["select"]:
        flag=False
        for i in user[str(message.from_user.id)]["search_result"]:
            if i[0] == message.text:
                base_url=i[1]
                #print(base_url)
                flag=True
                break
        
        if flag == True:
            temp = True
            try:
             all_links = requests.get("https://yst.am"+base_url)
            except Exception as e:
              all_links = requests.get("https://yts.ae"+base_url)
               
            if temp == True:
               page = BeautifulSoup(all_links.content, 'html.parser')
               try :
                  years=page.find("div",{"id":"movie-info"})
                  years=str(years)[0:150]
                  id = re.search('("\d+")',years).group().strip('"')
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
                  markup = types.ReplyKeyboardMarkup(row_width=4)
                  for i in range(len(quality)):
                    qua = str(quality[i]["quality"])+"\U0001F4C0"
                    url = quality[i]["url"]
                    size = str(quality[i]["size"])+"\U0001F4C2"
                    torrents.append((qua,size,url))
                    item = types.KeyboardButton(qua+"\n"+size)
                    markup.add(item)
                  #print(qua," ",url," ",size)
                  user[str(message.from_user.id)]["select"] = False    
                  user[str(message.from_user.id)]["quality"] = True
                  user[str(message.from_user.id)]["torrents"] = torrents
                  bot.send_photo(message.from_user.id, image_url)
                  bot.send_message(message.from_user.id,"Rating : {}\nRuntime : {}\nGenre : {}\nCertificate : {}".format(rating,run_time,genre,certificate))
                  bot.send_message(message.from_user.id, "Choose a quality:", reply_markup=markup)  
               except Exception as e: 
                  bot.send_message(message.from_user.id, "Movie you choose has been removed!try again\n")
                  user[str(message.from_user.id)]["search"] = True
               #print("\n\n\n\n id:::::",id)
               
        else:
            bot.send_message(message.from_user.id,"The movie is not found")
            user[str(message.from_user.id)]["search"] = True
      elif user[str(message.from_user.id)]["quality"]:
         flag = False
         val = message.text
         for torrent in user[str(message.from_user.id)]["torrents"]:
             if torrent[0] in val:
                 bot.reply_to(message,"Click here to download the torrent file \n " + torrent[2])
                 flag = True
         if flag == False:
                 bot.reply_to(message, message.from_user.first_name + ",please Enter the quality!\n Use /help ")  
         if user[str(message.from_user.id)]["select"] != False and user[str(message.from_user.id)]["search"] != False:
             user[str(message.from_user.id)]["quality"] = False
      else :
        bot.reply_to(message, message.from_user.first_name + ", Use /help ") 



@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://boiling-citadel-60592.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))      
      
