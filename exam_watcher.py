import os
import time
import requests
from twilio.rest import Client

# Twilio bilgilerini environment variables ile al
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
from_number = os.environ['FROM_NUMBER']  # whatsapp:+14155238886
to_number = os.environ['TO_NUMBER']      # whatsapp:+905428791644

client = Client(account_sid, auth_token)

# Kontrol edilecek site
url = "https://stdportal.emu.edu.tr/examlist.asp"

print("Script başladı, her 5 dakikada site kontrol edilecek...")

while True:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 200 değilse exception fırlatır
    except requests.RequestException:
        print("Siteye ulaşılamadı ❌")
    else:
        try:
            message = client.messages.create(
                body="Siteye ulaşıldı ✅",
                from_=from_number,
                to=to_number
            )
            print("Mesaj gönderildi:", message.sid)
        except Exception as e:
            print("Mesaj gönderilemedi ❌", e)
    
    # 5 dakika bekle (300 saniye)
    time.sleep(300)
