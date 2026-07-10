import time
import random
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# টেলিগ্রাম কনফিগারেশন
BOT_TOKEN = '8988002388:AAGrLEM2AbM9VjQvTSyjMAwnIJlUIHKKgZQ'
GROUP_ID = '-1003879489231'

# Render-এর পোর্ট সচল রাখার জন্য ডামী ওয়েব সার্ভার
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Payment Simulator Server is Active!")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyServer)
    server.serve_forever()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': GROUP_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def start_payment_simulator():
    print("🚀 পেমেন্ট সিমুলেটর বট সার্ভার থেকে চালু হচ্ছে...")
    send_telegram_message("⚙️ *SYSTEM UPDATE:* পেমেন্ট কনফার্মেশন বট সফলভাবে ক্লাউডে সেটআপ হয়েছে! প্রতি ৫-৭ সেকেন্ডে মেসেজ আসা শুরু হবে...")
    
    # সিমুলেশনের জন্য কিছু কাল্পনিক নাম ও ব্যাংকের লিস্ট
    names = ["Arif Khan", "Sumon Ahmed", "Mitu Akter", "Rakib Hasan", "Nadia Islam", "Tasnim Rahman", "Sabbir Hossain", "Fahim Shahriar"]
    methods = ["bKash App", "Nagad Wallet", "Rocket", "Upay", "Visa Card", "Mastercard"]
    
    while True:
        # র্যান্ডম ডাটা তৈরি
        customer = random.choice(names)
        pay_method = random.choice(methods)
        amount = random.randint(500, 15000)
        tx_id = f"TXN{random.randint(10000000, 99999999)}BD"
        
        # চমৎকার ফরম্যাটের পেমেন্ট মেসেজ
        msg = (
            f"✅ *PAYMENT COMPLETED* ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Customer:* {customer}\n"
            f"💰 *Amount Paid:* ৳{amount:,.2f} BDT\n"
            f"💳 *Method:* {pay_method}\n"
            f"🆔 *TrxID:* `{tx_id}`\n"
            f"🟢 *Status:* Successful\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            
        )
        
        # টেলিগ্রামে মেসেজ পাঠানো
        send_telegram_message(msg)
        
        # আপনার রিকোয়ারমেন্ট অনুযায়ী ৫ থেকেID ৭ সেকেন্ডের র্যান্ডম বিরতি (Sleep)
        sleep_time = random.randint(5, 7)
        time.sleep(sleep_time)

if __name__ == '__main__':
    # Render-এর পোর্ট ফিক্স রাখার জন্য ব্যাকগ্রাউন্ডে সার্ভার চালানো
    Thread(target=run_dummy_server, daemon=True).start()
    # পেমেন্ট মেসেজ পাঠানোর মেইন লুপ স্টার্ট
    start_payment_simulator()
