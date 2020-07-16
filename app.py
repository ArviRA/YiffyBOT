import telebot
import requests
from bs4 import BeautifulSoup
import requests
from telebot import types
import re
from flask import Flask,request
import json
import os

app = Flask(__name__)
start = False
search = False
select = False
quality = False
current_message = None
back = False
search_result = []
torrents = []
TOKEN = "1145940392:AAGAy_dEqfI0IXDTFiNPNZ_dagwYSAkJmYE"
bot = telebot.TeleBot(TOKEN)

#bot.set_webhook(url="http://example.com")
@bot.message_handler(commands=['start','help','search','back'])
def send_welcome(message):
    #print(message.text)
    global back,search,quality,select,current_message
    if(message.text == '/start'):
      #print(message)
      start = True
      quality = False
      bot.reply_to(message, "Welcome {}\n Enter /search to begin".format(message.from_user.first_name))
    elif(message.text == '/search'):
        global search
        search = True
        bot.reply_to(message,"Enter your movie name")
    elif(message.text == '/help'):
        bot.reply_to(message,"use /start to start the bot \n use /search for searching movies\n Then select the movies from the list\n use /back to go back to thee list \n select the Quality of movie\n download the torrent! have fun.")

    elif(message.text == '/back'): 
       if quality == True: 
            back = True
            search = True
            quality = False
            select = False
            #print("inside this module:::")
            #print(current_message)
            echo_all(current_message )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global search,select,search_result,quality,torrents
    if(search):
        base_url = ""
        #if back == False:
        current_message = message
        all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format(current_message.text))
        page = BeautifulSoup(all_links.content, 'html.parser')
        mydivs = page.findAll("a", {"class":"browse-movie-title"},href=True, text=True)
        years=page.findAll("div",{"class":"browse-movie-year"})
        search_result = []
        for i,j in zip(mydivs,years):
            dummy=i.text
            if "[" in dummy :
                dummy = dummy.split("] ")[1]
    
            search_result.append((dummy,j.text,i["href"]))
        
        #print(search,search_result)
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
    elif select:
        #print("after",message.text)
        flag=False
        for i in search_result:
            if i[0] in message.text:
                base_url=i[2]
                #print(base_url)
                flag=True
                break
        
        if flag == True:
            all_links = requests.get(base_url)
            page = BeautifulSoup(all_links.content, 'html.parser')
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
            select = False    
            quality = True
            bot.send_photo(message.from_user.id, image_url)
            bot.send_message(message.from_user.id,"Rating : {}\nRuntime : {}\nGenre : {}\nCertificate : {}".format(rating,run_time,genre,certificate))
            bot.send_message(message.from_user.id, "Choose a quality:", reply_markup=markup)

        elif flag == False:
            bot.reply_to(message,"The movie selected " + message.text + " is not in the list /help to begin")
    elif quality:
         flag = False
         val = message.text
         for torrent in torrents:
             if torrent[0] in val:
                 bot.reply_to(message,"Click here to download the torrent file \n " + torrent[2])
                 flag = True
         if flag == False:
                 bot.reply_to(message, message.from_user.first_name + ",please Enter the quality!\n Use /help ")  
         if select != False and search != False and start != False:
             quality = False
    else :
        bot.reply_to(message, message.from_user.first_name + ", Use /help ")
@app.route('/'+TOKEN,methods = ['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = 'https://boiling-citadel-60592.herokuapp.com/'+TOKEN)
    return '!',200
#bot.polling()
if __name__ == '__main__':
     port = int(os.environ.get('PORT', 5000))
     app.run(host='0.0.0.0', port=port)