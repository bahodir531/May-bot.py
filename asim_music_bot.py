from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pytube import Search, YouTube

api_id = 28780789
api_hash = "887f41df9181b9b355ba0b951447e2d2"
bot_token = "5412345688:AAENuR_PeKoiKs7yMxJairg-o6d7QvjJOsM"

app = Client("asim_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

keyboard = ReplyKeyboardMarkup(
    [["Musiqa qidirish"], ["Kino qidirish"]],
    resize_keyboard=True
)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Salom! Men Sanboyo Botman. Qanday yordam kerak?", reply_markup=keyboard)

@app.on_message(filters.text("Musiqa qidirish"))
def ask_music(client, message):
    message.reply_text("Qaysi qo‘shiqni izlaymiz? Ismini yozing.")

@app.on_message(filters.text("Kino qidirish"))
def ask_movie(client, message):
    message.reply_text("Qanday film qidiraylik? Nomini yozing.")

@app.on_message(filters.text & ~filters.command("start"))
def search_youtube(client, message):
    query = message.text
    message.reply_text(f"Qidirmoqdamiz: {query}...")
    try:
        results = Search(query).results
        if results:
            video = results[0]
            yt = YouTube(video.watch_url)
            title = yt.title
            stream = yt.streams.filter(only_audio=True).first()
            filename = yt.title + ".mp3"
            stream.download(filename=filename)
            message.reply_audio(audio=open(filename, "rb"), title=title)
        else:
            message.reply_text("Hech narsa topilmadi.")
    except Exception as e:
        message.reply_text(f"Xatolik yuz berdi: {e}")

app.run()
