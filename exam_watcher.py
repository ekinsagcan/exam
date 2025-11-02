import requests
from bs4 import BeautifulSoup
import hashlib
import time
from twilio.rest import Client

# --- Ayarlar ---
URL = "https://stdportal.emu.edu.tr/examlist.asp"
CHECK_INTERVAL = 60  # saniye

# Twilio bilgilerini kendi hesabından al
account_sid = "AC53d2c300fa0092e92f8be9528484b71e"
auth_token = "9adc5b6afa6972b0ced8280bfc187b4e"
from_number = "whatsapp:+14155238886"  # Twilio sandbox numarası

# Mesaj gidecek numaralar
to_numbers = [
    "whatsapp:+905428791644",
    "whatsapp:+905458631688"
]

client = Client(account_sid, auth_token)
previous_hash = None

def get_page_hash():
    """Sayfanın tablo içeriğini çekip hash değeri döner."""
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return None
    table_text = table.get_text(strip=True)
    return hashlib.md5(table_text.encode("utf-8")).hexdigest()

def send_whatsapp_message(msg):
    """Twilio üzerinden mesaj gönderir."""
    for number in to_numbers:
        client.messages.create(from_=from_number, body=msg, to=number)

print("🔍 Bot başlatıldı, sayfa her dakika kontrol ediliyor...")

while True:
    try:
        current_hash = get_page_hash()
        if current_hash and current_hash != previous_hash:
            if previous_hash is not None:
                message = f"📢 Yeni sınav takvimi yayınlandı!\n{URL}"
                send_whatsapp_message(message)
                print("✅ Değişiklik bulundu, mesaj gönderildi.")
            previous_hash = current_hash
        else:
            print("⏳ Değişiklik yok, tekrar kontrol edilecek...")
    except Exception as e:
        print("❌ Hata:", e)
    time.sleep(CHECK_INTERVAL)
