import os
from pyrogram import Client, filters
from pyrogram.types import InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp
from pytube import YouTube
from youtubesearchpython import VideosSearch
import requests

api_id = 'YOUR_API_ID'  # Telegram API ID
api_hash = 'YOUR_API_HASH'  # Telegram API HASH
bot_token = '7257260163:AAEO1xd-U0o0KHqRiunwskshlMGzCd2_iXc'  # Your Telegram Bot Token

app = Client("topvoldi_bot", api_id, api_hash, bot_token=bot_token)

# Start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply(
        "Assalomu alaykum! Men topvoldi_botman.\nMusiqa va video qidirib, yuklab beraman.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Musiqa qidirish", callback_data="search_music"),
             InlineKeyboardButton("Video qidirish", callback_data="search_video")]
        ])
    )

# Music search
@app.on_callback_query(filters.regex("search_music"))
def search_music(client, callback_query):
    callback_query.message.reply("Musiqani izlash uchun qidiring:")

# Video search
@app.on_callback_query(filters.regex("search_video"))
def search_video(client, callback_query):
    callback_query.message.reply("Videoni izlash uchun qidiring:")

# YouTube video downloader
@app.on_message(filters.text & filters.regex('^https://www.youtube.com/watch'))
def download_youtube(client, message):
    try:
        link = message.text
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path="downloads")
        message.reply("Video muvaffaqiyatli yuklandi!", quote=True)
    except Exception as e:
        message.reply(f"Xatolik yuz berdi: {str(e)}")

# Music search and download
@app.on_message(filters.text & filters.regex('^https://music.youtube.com/'))
def download_music(client, message):
    try:
        url = message.text
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        message.reply("Musiqa muvaffaqiyatli yuklandi!", quote=True)
    except Exception as e:
        message.reply(f"Xatolik yuz berdi: {str(e)}")

# Handle YouTube search
@app.on_message(filters.text)
def youtube_search(client, message):
    query = message.text
    video_search = VideosSearch(query, limit = 5)
    results = video_search.result()
    for video in results['videos']:
        video_title = video['title']
        video_url = video['link']
        message.reply(f"Video topildi: {video_title}\nLink: {video_url}", quote=True)

if __name__ == "__main__":
    app.run()
