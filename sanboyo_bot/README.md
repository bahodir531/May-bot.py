
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, I>
import yt_dlp
import os

API_ID = 28780789
API_HASH = "887f41df9181b9b355ba0b951447e2d2"
BOT_TOKEN = "5412345688:AAFIokS552zCjS8RZOBVe7YHDz>

bot = Client("media_bot", api_id=API_ID, api_hash=>

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Salom! Musiqa yoki v>

@bot.on_message(filters.text)
async def search(client, message):
    query = message.text
    buttons = [
        [InlineKeyboardButton("MP3 Yuklash", callb>
        [InlineKeyboardButton("Video HD Yuklash", >
    ]
    await message.reply("Qaysi formatda yuklamoqch>

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    format_type, query = data.split("|")
    msg = await callback_query.message.reply("Qidi>

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as >
            info = ydl.extract_info(f"ytsearch:{qu>
            url = info['webpage_url']

        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "quiet": True,
        }

        if format_type == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",