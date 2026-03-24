import telebot
import schedule
import time
import threading
from flask import Flask

# --- CONFIG BOT ---
TOKEN = "8723841678:AAFywlWPza3Tb3LeG9QZSmRsLt1JY01j9Es"
CHAT_ID = 1642810882
bot = telebot.TeleBot(TOKEN)

# --- FLASK SERVER (Keep Alive) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# --- PRONOS ---
def get_pronos():
    return """🔥 PRONOS DU JOUR 🔥
- Real Madrid vs Barça : Real gagne / BTTS Oui / Over 2.5
- Liverpool vs Man City : BTTS Oui / Over 2.5 / 1X
- PSG vs Lyon : PSG gagne / Over 2.5 / BTTS Oui

✅ Combiné SAFE :
Real gagne + PSG gagne + BTTS Liverpool-City

💎 Combiné VALUE :
Over 2.5 Real-Barça + BTTS PSG-Lyon + 1X Liverpool

⚠ Pariez responsablement.
"""

# --- ENVOI AUTOMATIQUE ---
def send_pronos():
    bot.send_message(CHAT_ID, get_pronos())

# --- COMMANDES ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenue ! Commandes :\n/pronos - Pronostics du jour\n/combine - Combinés SAFE & VALUE")

@bot.message_handler(commands=['pronos'])
def send_pronos_command(message):
    bot.send_message(message.chat.id, get_pronos())

@bot.message_handler(commands=['combine'])
def send_combine_command(message):
    bot.send_message(message.chat.id, "✅ Combiné SAFE :\nReal gagne + PSG gagne + BTTS Liverpool-City\n\n💎 Combiné VALUE :\nOver 2.5 Real-Barça + BTTS PSG-Lyon + 1X Liverpool")

# --- PLANIFICATION ---
schedule.every().day.at("10:40").do(send_pronos)
schedule.every().day.at("12:00").do(send_pronos)
schedule.every().day.at("14:00").do(send_pronos)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- THREADS ---
def start_bot():
    print("Bot is running!")
    bot.polling(none_stop=True)

threading.Thread(target=run_schedule).start()
threading.Thread(target=start_bot).start()

# --- LANCER FLASK ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
