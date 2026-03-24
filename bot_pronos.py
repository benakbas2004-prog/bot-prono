import telebot
import schedule
import time
import threading
from flask import Flask
import requests
import random

# --- CONFIG BOT ---
TOKEN = "8723841678:AAFywlWPza3Tb3LeG9QZSmRsLt1JY01j9Es"
CHAT_ID = 1642810882
bot = telebot.TeleBot(TOKEN)

# --- CONFIG API-FOOTBALL ---
API_KEY = "965d24100fde96d7b00b28d4241610ad"
API_URL = "https://v3.football.api-sports.io/fixtures?date=today"

headers = {
    "x-apisports-key": API_KEY
}

# --- FLASK SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# --- GENERER LES PRONOS AUTOMATIQUES ---
def get_pronos_from_api():
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json().get("response", [])
            if not data:
                return "⚠ Aucun match trouvé aujourd'hui."
            
            pronos = []
            for match in data[:5]:  # On prend les 5 premiers matchs
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]
                # Génération aléatoire simple (peut être améliorée avec stats)
                choix = random.choice(["1", "X", "2"])
                over = random.choice(["Over 2.5", "Under 2.5"])
                btts = random.choice(["BTTS Oui", "BTTS Non"])
                pronos.append(f"{home} vs {away} : {choix} / {over} / {btts}")
            
            return "🔥 PRONOS DU JOUR 🔥\n" + "\n".join(pronos)
        else:
            return f"Erreur API : {response.status_code}"
    except Exception as e:
        return f"Erreur : {e}"

# --- ENVOI AUTOMATIQUE ---
def send_pronos():
    bot.send_message(CHAT_ID, get_pronos_from_api())

# --- COMMANDES ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenue ! Commandes :\n/pronos - Pronostics du jour\n/combine - Combinés SAFE & VALUE")

@bot.message_handler(commands=['pronos'])
def send_pronos_command(message):
    bot.send_message(message.chat.id, get_pronos_from_api())

@bot.message_handler(commands=['combine'])
def send_combine_command(message):
    bot.send_message(message.chat.id, "✅ Combiné SAFE :\nSélection des meilleurs pronos\n💎 Combiné VALUE :\nSélection value bets")

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
