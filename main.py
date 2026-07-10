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

# সাধারণ মেসেজ পাঠানোর ফাংশন
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

# নির্দিষ্ট মেসেজে রিপ্লাই দিয়ে মেসেজ পাঠানোর ফাংশan
def send_telegram_reply(text, reply_to_message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': GROUP_ID, 
        'text': text, 
        'parse_mode': 'Markdown',
        'reply_to_message_id': reply_to_message_id  # এই আইডিটি রিপ্লাই করতে সাহায্য করে
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Reply Error: {e}")

def start_withdrawal_simulator():
    print("🚀 উইথড্র সিমুলেটর বট সার্ভার থেকে চালু হচ্ছে...")
    send_telegram_message("⚙️ *SYSTEM UPDATE:* উইথড্র রিকোয়েস্ট ও রিপ্লাই কমপ্লিট সিস্টেম সফলভাবে ক্লাউডে সেটআপ হয়েছে!")
    
    # সিমুলেশনের জন্য ডেটা লিস্ট
    names = ["Arif Khan", "Sumon Ahmed", "Mitu Akter", "Rakib Hasan", "Nadia Islam", "Tasnim Rahman", "Sabbir Hossain", "Fahim Shahriar"]
    wallets = ["bKash (Personal)", "Nagad (Personal)", "Rocket (Personal)", "Upay Wallet", "Binance Pay ID", "TRC20 Wallet"]
    
    while True:
        # র্যান্ডম ডেটা জেনারেট করা
        customer = random.choice(names)
        wallet_type = random.choice(wallets)
        amount = random.randint(1000, 25000)
        tx_id = f"WTH{random.randint(100000, 999999)}BD"
        
        # বর্তমান লাইভ সময় (ঘন্টা:মিনিট:সেকেন্ড) বের করা
        current_time = datetime.now().strftime("%I:%M:%S %p")
        
        # ১. উইথড্র রিকোয়েস্ট মেসেজ তৈরি
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
        
        # রিকোয়েস্ট মেসেজ পাঠিয়ে তার ID সংগ্রহ করা
        request_message_id = send_telegram_message(request_msg)
        
        # যদি রিকোয়েস্ট মেসেজটি সফলভাবে গ্রুপে যায়, তবে ৫-৭ সেকেন্ড অপেক্ষা করে রিপ্লাই পাঠানো হবে
        if request_message_id:
            # আপনার রিকোয়ারমেন্ট অনুযায়ী ৫ থেকে ৭ সেকেন্ডের র্যান্ডম বিরতি (Sleep)
            sleep_time = random.randint(5, 7)
            time.sleep(sleep_time)
            
            # উইথড্র কমপ্লিট হওয়ার লাইভ সময় (ঘন্টা:মিনিট:সেকেন্ড)
            complete_time = datetime.now().strftime("%I:%M:%S %p")
            
            # ২. উইথড্র কমপ্লিট মেসেজ তৈরি (যা রিকোয়েস্টের রিপ্লাই হিসেবে যাবে)
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
            
            # রিকোয়েস্ট মেসেজের নিচে রিপ্লাই হিসেবে পাঠানো
            send_telegram_reply(complete_msg, request_message_id)
            
        # পরবর্তী নতুন রিকোয়েস্ট আসার আগে আরও ৫ থেকে ৭ সেকেন্ডের বিরতি
        time.sleep(random.randint(5, 7))

if __name__ == '__main__':
    # Render-এর পোর্ট সচল রাখতে ব্যাকগ্রাউন্ডে ডামী ওয়েব সার্ভার চালু
    Thread(target=run_dummy_server, daemon=True).start()
    # উইথড্র মেইন ইঞ্জিন চালু
    start_withdrawal_simulator()
