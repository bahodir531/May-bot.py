from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os

# Botni sozlash
bot = Client(
    "topvoldi_bot",
    api_id=28780789,
    api_hash="887f41df9181b9b355ba0b951447e2d2",
    bot_token="7257260163:AAEO1xd-U0o0KHqRiunwskshlMGzCd2_iXc"
)

# Start komandasi
@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply(
        "Salom! Qidiriladigan fayl turini tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 Musiqa Qidirish", callback_data="music")],
            [InlineKeyboardButton("🎬 Kino Qidirish", callback_data="video")]
        ])
    )

# Musiqa va kino tanlash tugmalari
@bot.on_callback_query()
async def query_handler(client, callback_query):
    if callback_query.data == "music":
        await callback_query.message.reply("Musiqa nomini yuboring:")
    elif callback_query.data == "video":
        await callback_query.message.reply("Kino nomini yuboring:")

# Musiqa va video qidirish va yuklab olish
@bot.on_message(filters.text & ~filters.command(["start"]))
async def download_media(client, message: Message):
    query = message.text
    msg = await message.reply("Qidirilmoqda, kuting...")

    # YouTube dan yuklab olish sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['webpage_url']
            title = info.get('title', 'no-title')

        await msg.edit(f"Topildi: {title}\nYuklab olinmoqda...")

        # Yuklab olish
        ydl_opts.update({'outtmpl': f'{title}.%(ext)s'})
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        filename = f"{title}.webm"
        if os.path.exists(filename):
            await message.reply_document(filename, caption=title)
            os.remove(filename)
        else:
            await message.reply("Xatolik: fayl topilmadi.")
    except Exception as e:
        await msg.edit(f"Xatolik: {e}")

# Botni ishga tushurish
bot.run()
