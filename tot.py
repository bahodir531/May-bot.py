
import os
from pyrogram import Client, filters
import yt_dlp

# Telegram API ma'lumotlari
api_id = 28780789  # O'zingizni API ID bilan almashtiring
api_hash = '887f41df9181b9b355ba0b951447e2d2'  # O'zingizni API hash bilan almashtiring
bot_token = '6155004394:AAHvSSBp5rpgBGg0Svgyhp9Fq8FnFB3AL6U'  # O'zingizni Bot Token bilan almashtiring

# Botni yaratish
bot = Client("video_music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Video yoki musiqa yuklash funksiyasi
def download_video(url, download_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': download_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, download_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Komanda qo'shish - Musiqa qidirish
@bot.on_message(filters.command('music'))
async def music_search(client, message):
    query = message.text.split(" ", 1)[1]  # Qidirish so'rovini olish
    if query:
        await message.reply("Qidiryapman...")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        download_audio(search_url, "downloaded_audio.mp3")
        await message.reply_document("downloaded_audio.mp3")
    else:
        await message.reply("Iltimos, musiqa nomini kiriting!")

# Komanda qo'shish - Kino qidirish
@bot.on_message(filters.command('movie'))
async def movie_search(client, message):
    query = message.text.split(" ", 1)[1]  # Qidirish so'rovini olish
    if query:
        await message.reply("Qidiryapman...")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        download_video(search_url, "downloaded_movie.mp4")
        await message.reply_document("downloaded_movie.mp4")
    else:
        await message.reply("Iltimos, kino nomini kiriting!")

# Botni ishga tushirish
bot.run()
