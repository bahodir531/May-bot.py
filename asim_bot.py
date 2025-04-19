from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os

api_id = 28780789
api_hash = "887f41df9181b9b355ba0b951447e2d2"
bot_token = "5412345688:AAENuR_PeKoiKs7yMxJairg-o6d7QvjJOsM"

app = Client("asim_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Salom! Men Asim botman. Nima kerak?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Musiqa Qidirish", callback_data="music")],
            [InlineKeyboardButton("Kino Qidirish", callback_data="movie")]
        ])
    )

@app.on_callback_query()
async def callback_query(client, callback_query):
    if callback_query.data == "music":
        await callback_query.message.reply("Musiqa nomini yuboring.")
    elif callback_query.data == "movie":
        await callback_query.message.reply("Kino nomini yuboring.")

@app.on_message(filters.text & ~filters.command("start"))
async def search_and_send(client, message):
    query = message.text
    search = VideosSearch(query, limit=1)
    result = search.result()["result"][0]
    link = result["link"]
    title = result["title"]
    
    await message.reply(f"Topildi: {title}\nYuklab olinmoqda...")

    try:
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(filename="audio.mp4")

        os.rename("audio.mp4", "audio.mp3")
        await client.send_audio(message.chat.id, "audio.mp3", title=title)
        os.remove("audio.mp3")
    except Exception as e:
        await message.reply(f"Xatolik: {str(e)}")

app.run()
