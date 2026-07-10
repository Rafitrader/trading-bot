import time
import random
import requests
from datetime import datetime
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
        self.wfile.write(b"Withdrawal Simulator Server is Active!")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyServer)
    server.serve_forever()

# সাধারণ মেসেজ পাঠানোর ফাংশন (রিকোয়েস্টের জন্য)
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': GROUP_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        response = requests.post(url, json=payload, timeout=10).json()
        if response.get("ok"):
            return response["result"]["message_id"]
    except Exception as e:
        print(f"Telegram Send Error: {e}")
    return None

# নির্দিষ্ট মেসেজে রিপ্লাই দিয়ে মেসেজ পাঠানোর ফাংশন (কমপ্লিট করার জন্য)
def send_telegram_reply(text, reply_to_message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': GROUP_ID, 
        'text': text, 
        'parse_mode': 'Markdown',
        'reply_to_message_id': reply_to_message_id
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Reply Error: {e}")

def start_withdrawal_simulator():
    print("🚀 উইথড্র সিমুলেটর বট সার্ভার থেকে চালু হচ্ছে...")
    send_telegram_message("⚙️ *SYSTEM UPDATE:* টাইমিং মডিফিকেশন সফলভাবে আপডেট করা হয়েছে!\n⏱️ _Request: 10-12s | Reply: 20-22s_")
    
    names = ["Arif Khan", "Sumon Ahmed", "Mitu Akter", "Rakib Hasan", "Nadia Islam", "Tasnim Rahman", "Sabbir Hossain", "Fahim Shahriar"]
    wallets = ["bKash (Personal)", "Nagad (Personal)", "Rocket (Personal)", "Upay Wallet", "Binance Pay ID", "TRC20 Wallet"]
    
    while True:
        customer = random.choice(names)
        wallet_type = random.choice(wallets)
        amount = random.randint(1000, 25000)
        tx_id = f"WTH{random.randint(100000, 999999)}BD"
        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        
        # ১. উইথড্র রিকোয়েস্ট মেসেজ
        request_msg = (
            f"📥 *WITHDRAWAL REQUEST* 📥\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *User:* {customer}\n"
            f"💰 *Amount:* ৳{amount:,.2f} BDT\n"
            f"💳 *Method:* {wallet_type}\n"
            f"🕒 *Req Time:* {current_time}\n"
            f"🆔 *Withdraw ID:* `{tx_id}`\n"
            f"🟡 *Status:* Pending Approval\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 _Render অটোমেটেড রিকোয়েস্ট সিস্টেম।_"
        )
        
        request_message_id = send_telegram_message(request_msg)
        
        if request_message_id:
            # 👉 আপনার রিকোয়ারমেন্ট অনুযায়ী ২০ থেকে ২২ সেকেন্ডের র্যান্ডম বিরতি (কমপ্লিট মেসেজের জন্য)
            reply_sleep = random.randint(20, 22)
            time.sleep(reply_sleep)
            
            complete_time = datetime.now().strftime("%I:%M:%S %p")
            
            # ২. উইথড্র কমপ্লিট মেসেজ (যা রিকোয়েস্টের রিপ্লাই হিসেবে যাবে)
            complete_msg = (
                f"✅ *WITHDRAWAL COMPLETED* ✅\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 *User:* {customer}\n"
                f"💰 *Amount Sent:* ৳{amount:,.2f} BDT\n"
                f"💳 *Method:* {wallet_type}\n"
                f"🕒 *Done Time:* {complete_time}\n"
                f"🆔 *Withdraw ID:* `{tx_id}`\n"
                f"🟢 *Status:* Successfully Paid\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💵 _টাকা সফলভাবে ওয়ালেটে পাঠিয়ে দেওয়া হয়েছে!_"
            )
            
            send_telegram_reply(complete_msg, request_message_id)
            
        # 👉 আপনার রিকোয়ারমেন্ট অনুযায়ী পরবর্তী নতুন রিকোয়েস্ট আসার আগে ১০ থেকে ১২ সেকেন্ডের বিরতি
        next_request_sleep = random.randint(10, 12)
        time.sleep(next_request_sleep)

if __name__ == '__main__':
    Thread(target=run_dummy_server, daemon=True).start()
    start_withdrawal_simulator()                f"✅ *WITHDRAWAL COMPLETED* ✅\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 *User:* {customer}\n"
                f"💰 *Amount Sent:* ৳{amount:,.2f} BDT\n"
                f"💳 *Method:* {wallet_type}\n"
                f"🕒 *Done Time:* {complete_time}\n"
                f"🆔 *Withdraw ID:* `{tx_id}`\n"
                f"🟢 *Status:* Successfully Paid\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💵 _টাকা সফলভাবে ওয়ালেটে পাঠিয়ে দেওয়া হয়েছে!_"
            )
            
            # রিকোয়েস্ট মেসেজের নিচে রিপ্লাই হিসেবে পাঠানো
            send_telegram_reply(complete_msg, request_message_id)
            
        # পরবর্তী নতুন রিকোয়েস্ট আসার আগে আরও ৫ থেকে ৭ সেকেন্ডের বিরতি
        time.sleep(random.randint(5, 7))

if __name__ == '__main__':
    # Render-এর পোর্ট সচল রাখতে ব্যাকগ্রাউন্ডে ডামী ওয়েব সার্ভার চালু
    Thread(target=run_dummy_server, daemon=True).start()
    # উইথড্র মেইন ইঞ্জিন চালু
    start_withdrawal_simulator()
