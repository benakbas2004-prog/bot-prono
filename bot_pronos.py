import requests
import schedule
import time
from datetime import datetime

# ✅ Ton token Telegram et chat_id
TOKEN = "8723841678:AAFywlWPza3Tb3LeG9QZSmRsLt1JY01j9Es"
CHAT_ID = "1642810882"
URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ✅ Clé API-Football
API_KEY = "965d24100fde96d7b00b28d4241610ad"
API_URL = "https://v3.football.api-sports.io/fixtures"

HEADERS = {
    "x-apisports-key": API_KEY
}

# ✅ Fonction pour envoyer un message Telegram
def envoyer_message(message):
    try:
        requests.post(URL_TELEGRAM, data={"chat_id": CHAT_ID, "text": message})
        print(f"[{datetime.now()}] Message envoyé : {message}")
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

# ✅ Récupérer les matchs du jour (Foot)
def get_matchs_foot():
    today = datetime.now().strftime("%Y-%m-%d")
    params = {"date": today, "league": 61, "season": 2023}  # Ligue 1 exemple
    response = requests.get(API_URL, headers=HEADERS, params=params)
    data = response.json()
    matchs = []
    if "response" in data:
        for match in data["response"][:3]:  # 3 matchs max
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            matchs.append(f"{home} vs {away}")
    return matchs if matchs else ["Pas de match trouvé"]

# ✅ Générer pronostics Foot
def generer_pronos_foot():
    matchs = get_matchs_foot()
    pronos = "⚽ Pronostics Foot du jour :\n"
    for m in matchs:
        pronos += f"✅ {m} → Victoire {m.split(' vs ')[0]}\n"
    pronos += "\n💡 Conseil : Mise prudente en simple, combiné 2 matchs max."
    return pronos

# ✅ Basket & Tennis (statique pour l'instant)
def generer_pronos_basket():
    return """🏀 Pronostics Basket du jour :
✅ Lakers vs Warriors : +210.5 points
🔥 Boston gagne (Cote 1.70)
💡 Conseil : Value Bet sur Boston"""

def generer_pronos_tennis():
    return """🎾 Pronostics Tennis du jour :
✅ Djokovic gagne 2-0 (Cote 1.50)
🔥 Alcaraz + Over 21.5 jeux (Cote 1.85)
💡 Conseil : Parier en simple pour sécuriser"""

# ✅ Fonctions d'envoi
def pronos_basket():
    envoyer_message(generer_pronos_basket())

def pronos_foot():
    envoyer_message(generer_pronos_foot())

def pronos_tennis():
    envoyer_message(generer_pronos_tennis())

# ✅ Programmation des horaires
schedule.every().day.at("10:00").do(pronos_basket)
schedule.every().day.at("13:00").do(pronos_foot)
schedule.every().day.at("14:00").do(pronos_tennis)

print("✅ Bot IA dynamique lancé...")
envoyer_message("🚀 Test réussi : ton bot est bien en ligne sur Render ✅")


while True:
    schedule.run_pending()
    time.sleep(60)
