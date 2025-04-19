import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from youtubesearchpython import VideosSearch

# Siz bergan bot token
bot = telebot.TeleBot("5412345688:AAENuR_PeKoiKs7yMxJairg-o6d7QvjJOsM")

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎵 Musiqa topish"), KeyboardButton("🎬 Kino topish"))
    bot.send_message(message.chat.id, "Salom! Nima topay?", reply_markup=markup)

# Asosiy tugmalarni ishlovchi qism
@bot.message_handler(func=lambda message: True)
def search(message):
    if message.text == "🎵 Musiqa topish":
        bot.send_message(message.chat.id, "Qaysi musiqani qidiray?")
        bot.register_next_step_handler(message, search_music)
    elif message.text == "🎬 Kino topish":
        bot.send_message(message.chat.id, "Qanday kino qidiray?")
        bot.register_next_step_handler(message, search_movie)

def search_music(message):
    query = message.text
    results = VideosSearch(query + " music", limit=1).result()
    if results['result']:
        link = results['result'][0]['link']
        bot.send_message(message.chat.id, f"Musiqa topildi:\n{link}")
    else:
        bot.send_message(message.chat.id, "Hech narsa topilmadi.")

def search_movie(message):
    query = message.text
    results = VideosSearch(query + " film", limit=1).result()
    if results['result']:
        link = results['result'][0]['link']
        bot.send_message(message.chat.id, f"Kino topildi:\n{link}")
    else:
        bot.send_message(message.chat.id, "Hech narsa topilmadi.")

bot.polling()
