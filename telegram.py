import telebot
from bs4 import BeautifulSoup
import requests
bot = telebot.TeleBot("1145940392:AAGAy_dEqfI0IXDTFiNPNZ_dagwYSAkJmYE")

#bot.set_webhook(url="http://example.com")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome {}\n Enter the Movie Name".format(message.from_user.first_name))

    #print(message.from_user.id)
    #updates=bot.get_updates()
    #print(updates)
	#bot.reply_to(message, "https://yts.mx/torrent/download/3D1ADE5E738AEE2ACA577B9D922B0E2903159BE7")
    #bot.send_photo(message.from_user.id, "https://spiderimg.amarujala.com/assets/images/2017/01/26/750x506/_1485422033.jpeg")
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    movie=message.text
    print("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format(movie))
    all_links = requests.get("https://yts.mx/browse-movies/{}/all/all/0/latest/0/all".format(movie))
    print(all_links)
    page = BeautifulSoup(all_links, 'html.parser')
    print(page.prettify())
    my_div=soup.findAll('a')
    for div in my_div:
     if(div['class']=='browse-movie-title'):
           print(div)
    #bot.reply_to(message, message.from_user.first_name)

bot.polling()