from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token va API ma'lumotlar
API_ID = 28780789
API_HASH = "887f41df9181b9b355ba0b951447e2d2"
BOT_TOKEN = "7257260163:AAEO1xd-U0o0KHqRiunwskshlMGzCd2_iXc"

# Bot ishga tushiriladi
app = Client("topvoldi_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


# /start yoki /menu komandasi
@app.on_message(filters.command(["start", "menu"]))
async def menu_handler(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 A'zolar soni", callback_data="members")],
        [InlineKeyboardButton("🛡️ Adminlar ro'yxati", callback_data="admins")]
    ])
    await message.reply("Salom! Quyidagilardan birini tanlang:", reply_markup=keyboard)


# Tugmalar bosilganda javob
@app.on_callback_query()
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id

    if callback_query.data == "members":
        count = await client.get_chat_members_count(chat_id)
        await callback_query.message.edit_text(f"👥 Guruhda jami {count} ta a'zo bor.")

    elif callback_query.data == "admins":
        admins = await client.get_chat_administrators(chat_id)
        text = "🛡️ Guruh adminlari:\n\n"
        text += "\n".join([f"- {admin.user.first_name}" for admin in admins])
        await callback_query.message.edit_text(text)


# Kim yangi a'zoni qo‘shganini ko‘rsatish
@app.on_message(filters.new_chat_members)
async def new_member_handler(client, message):
    for user in message.new_chat_members:
        adder = message.from_user
        await message.reply(
            f"➕ {user.mention} ni {adder.mention} guruhga qo‘shdi."
        )


app.run()
