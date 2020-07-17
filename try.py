import requests
import os
from bs4 import BeautifulSoup
import telebot
import json
import os
from telebot import types
from flask import Flask, request

TOKEN = '1010311458:AAFiDsa4J4pYXAi8UOblX2Vo3D7V8RhuvHg'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

def sendMessage(message, text):
   bot.send_message(message.chat.id, text)
# This method will send a message formatted in HTML to the user whenever it starts the bot with the /start command, feel free to add as many commands' handlers as you want
@bot.message_handler(commands=['start'])
def send_info(message):
   text = (
   "<b>Welcome to the Yify BOt 🤖!</b>\n"
   "Say /help to the bot to get to know about it!"
   )
   summa=requests.get("https://yts.mx/api/v2/movie_details.json?movie_id=31706")
   print("\n\n\n:mx api",summa)
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


# This method will fire whenever the bot receives a message from a user, it will check that there is actually a not empty string in it and, in this case, it will check if there is the 'hello' word in it, if so it will reply with the message we defined
@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
   if 'hello'in message.text.lower():
      sendMessage(message, 'Hello! How are you doing today?')
   else:
        base_url = ""
        #if back == False:
        current_message = message
        print("\n\n\n message ",message.text,"\n\n\n")
        all_links = requests.get("https://yts.pm/browse-movies/{}/all/all/0/latest".format(message.text))
        print(all_links)
        page = BeautifulSoup(all_links.content, 'html.parser')
        mydivs = page.findAll("a", {"class":"browse-movie-title"},href=True, text=True)
        years=page.findAll("div",{"class":"browse-movie-year"})
        print("\n\n\n\nMy div",mydivs,"\n\n\n\n")
        search_result = []
        for i,j in zip(mydivs,years):
            dummy=i.text
            if "[" in dummy :
                dummy = dummy.split("] ")[1] 
    
            search_result.append((dummy,j.text,i["href"]))
        
        print("\n\n\n\n search result",search_result)
        start = False
        search = False
        select = True
        markup = types.ReplyKeyboardMarkup(row_width=4)
        #print(search_result)
        if len(search_result) != 0:
            for i in search_result:
                keyword = str (i[0] + " " + i[1])
                item = types.KeyboardButton(keyword)
                markup.add(item)
            bot.send_message(current_message.from_user.id, "Choose a movie:", reply_markup=markup)
        else :
            bot.reply_to(current_message, current_message.from_user.first_name + ",No such movies are present! try again\n /search")   

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
      
