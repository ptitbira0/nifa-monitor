import requests
import hashlib
import time
from datetime import datetime
from twilio.rest import Client

# Configuration Twilio
ACCOUNT_SID = "AC61c05c15f806f8a611dee4ede9111a42"
AUTH_TOKEN = "118a6692782ed4f1a382d6293e38885b"
TWILIO_WHATSAPP = "whatsapp:+14155238886"  # Numéro sandbox Twilio
TON_WHATSAPP = "whatsapp:+221774976257"

# URL à surveiller
URL = "https://www.nifa.sn/trajets-disponibles"

# Jours à surveiller (0=lundi, 1=mardi, 2=mercredi)
JOURS_ACTIFS = [0, 1, 2]

def get_page_hash():
    try:
        response = requests.get(URL, timeout=15)
        return hashlib.md5(response.text.encode()).hexdigest()
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")
        return None

def envoyer_whatsapp(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP,
        to=TON_WHATSAPP
    )
    print(f"WhatsApp envoyé: {message}")

def main():
    print("🚌 Surveillance NIFA démarrée...")
    ancien_hash = get_page_hash()
    
    while True:
        now = datetime.now()
        jour = now.weekday()  # 0=lundi, 6=dimanche
        
        if jour in JOURS_ACTIFS:
            nouveau_hash = get_page_hash()
            
            if nouveau_hash and ancien_hash and nouveau_hash != ancien_hash:
                message = "🚌 NIFA - La page des trajets a changé ! Des places sont peut-être disponibles. Réserve vite : https://www.nifa.sn/trajets-disponibles"
                envoyer_whatsapp(message)
                ancien_hash = nouveau_hash
            elif nouveau_hash:
                ancien_hash = nouveau_hash
                
            print(f"[{now.strftime('%H:%M:%S')}] Vérification effectuée - Jour: {now.strftime('%A')}")
        else:
            print(f"[{now.strftime('%H:%M:%S')}] Jour inactif ({now.strftime('%A')}) - Pause")
        
        time.sleep(300)  # Vérification toutes les 5 minutes

if __name__ == "__main__":
    main()
