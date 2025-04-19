from pyrogram import Client, filters
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os

api_id = 28780789
api_hash = "887f41df9181b9b355ba0b951447e2d2"
bot_token = "7525194564:AAEkwCbzu04lWbX0Gk6fdoIMm-Djt2KOG-c"

app = Client("vkm_clone", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start_handler(client, message):
    message.reply(
        "Salom! Men VKMusic bot cloneman!\n"
        "Musiqa nomini yuboring, men sizga MP3 formatda topib beraman."
    )

@app.on_message(filters.text & ~filters.command(["start"]))
def music_search(client, message):
    query = message.text
    user = message.from_user.first_name
    message.reply(f"🔍 '{query}' uchun musiqa qidirilmoqda...")

    try:
        search = VideosSearch(query, limit=1)
        result = search.result()["result"][0]
        title = result["title"]
        link = result["link"]

        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        file_path = stream.download(filename="music.mp4")

        # MP4ni MP3ga o‘tkazish
        os.system("ffmpeg -i music.mp4 -vn -ab 128k -ar 44100 -y music.mp3")

        message.reply_audio("music.mp3", title=title, performer=yt.author)

        # Tozalash
        os.remove("music.mp4")
        os.remove("music.mp3")

    except Exception as e:
        message.reply(f"Xatolik yuz berdi: {e}")

app.run()
