from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os

# Telegram API ma'lumotlaringiz
api_id = 28780789
api_hash = "887f41df9181b9b355ba0b951447e2d2"
bot_token = "7525194564:AAEkwCbzu04lWbX0Gk6fdoIMm-Djt2KOG-c"

app = Client("topvoldi_vkm", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start komandasi
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Salom! Musiqa nomini yuboring yoki video link tashlang!")

# YouTube qidiruv va tugmalar
@app.on_message(filters.text & ~filters.command(["start"]))
def search_music(client, message):
    text = message.text

    # Instagram yoki TikTok videosi yuklash
    if "instagram.com" in text or "tiktok.com" in text:
        message.reply("⏬ Video yuklanmoqda...")
        try:
            os.system(f"yt-dlp -o 'downloaded_video.mp4' {text}")
            message.reply_video("downloaded_video.mp4", caption="✅ Mana video!")
            os.remove("downloaded_video.mp4")
        except Exception as e:
            message.reply(f"Xatolik: {e}")
        return

    # YouTube qidiruv natijalari
    search = VideosSearch(text, limit=5)
    results = search.result()["result"]
    buttons = []

    for result in results:
        title = result["title"][:40]
        video_id = result["id"]
        buttons.append([
            InlineKeyboardButton("▶️ Tingla", callback_data=f"audio_{video_id}"),
            InlineKeyboardButton("📹 Video", callback_data=f"video_{video_id}")
        ])

    message.reply("Quyidagilardan birini tanlang:", reply_markup=InlineKeyboardMarkup(buttons))

# Audio yuklash
@app.on_callback_query(filters.regex("^audio_"))
def send_audio(client, callback_query: CallbackQuery):
    video_id = callback_query.data.split("_")[1]
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        yt = YouTube(url)
        title = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename="music.mp4")

        os.system("ffmpeg -i music.mp4 -vn -ab 128k -ar 44100 -y music.mp3")
        callback_query.message.reply_audio("music.mp3", title=title, performer=yt.author)

        os.remove("music.mp4")
        os.remove("music.mp3")
    except Exception as e:
        callback_query.message.reply(f"Xatolik: {e}")
    callback_query.answer()

# Video yuklash
@app.on_callback_query(filters.regex("^video_"))
def send_video(client, callback_query: CallbackQuery):
    video_id = callback_query.data.split("_")[1]
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        os.system(f"yt-dlp -f mp4 -o 'video.mp4' {url}")
        callback_query.message.reply_video("video.mp4", caption="Mana video!")
        os.remove("video.mp4")
    except Exception as e:
        callback_query.message.reply(f"Xatolik: {e}")
    callback_query.answer()

app.run()
