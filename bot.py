from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp
import os

API_ID = 28780789
API_HASH = "887f41df9181b9b355ba0b951447e2d2"
BOT_TOKEN = "5412345688:AAFIokS552zCjS8RZOBVe7YHDzqTB6fouBM"

bot = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Salom! Musiqa yoki video nomini yuboring:")

@bot.on_message(filters.text)
async def search(client, message):
    query = message.text
    buttons = [
        [InlineKeyboardButton("MP3 Yuklash", callback_data=f"mp3|{query}")],
        [InlineKeyboardButton("Video HD Yuklash", callback_data=f"video|{query}")]
    ]
    await message.reply("Qaysi formatda yuklamoqchisiz?", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    format_type, query = data.split("|")
    msg = await callback_query.message.reply("Qidirilmoqda...")

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
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
                    "preferredquality": "192",
                }],
            })
        else:
            ydl_opts.update({"format": "best[ext=mp4]"})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            file_path = ydl.prepare_filename(info)
            if format_type == "mp3":
                file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")

        await msg.edit("Yuklanmoqda...")
        await client.send_document(callback_query.message.chat.id, document=file_path, caption=info["title"])
        os.remove(file_path)

    except Exception as e:
        await msg.edit(f"Xatolik: {e}")

bot.run()
