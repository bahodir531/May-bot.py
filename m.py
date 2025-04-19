from pyrogram import Client, filters
import random

api_id = 28780789
api_hash = "887f41df9181b9b355ba0b951447e2d2"
bot_token = "7525194564:AAEkwCbzu04lWbX0Gk6fdoIMm-Djt2KOG-c"  # Siz bergan token

app = Client("math_game_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Global o'yin holati
current_game = {
    "question": None,
    "answer": None,
    "active": False
}

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Salom! Bu multiplayer matematik o‘yin.\n/startgame bilan o‘yin boshlang!")

@app.on_message(filters.command("startgame"))
def start_game(client, message):
    if current_game["active"]:
        message.reply("O'yin allaqachon boshlangan!")
        return

    a = random.randint(1, 20)
    b = random.randint(1, 20)
    current_game["question"] = f"{a} + {b}"
    current_game["answer"] = str(a + b)
    current_game["active"] = True

    message.reply(f"Kim birinchi to‘g‘ri javob beradi?\nSavol: {current_game['question']}")

@app.on_message(filters.text & ~filters.command(["start", "startgame"]))
def answer_handler(client, message):
    if current_game["active"] and message.text.strip() == current_game["answer"]:
        message.reply(f"To‘g‘ri javob! {message.from_user.first_name} g‘olib!")
        current_game["active"] = False
        current_game["question"] = None
        current_game["answer"] = None
    elif current_game["active"]:
        pass  # noto‘g‘ri javoblar sukut bilan qabul qilinadi
    else:
        message.reply("Hozircha hech qanday o‘yin yo‘q. /startgame bilan boshlang.")

app.run()
