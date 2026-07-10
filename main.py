import time
import requests
import random
import string
from datetime import datetime

# আপনার দেওয়া সঠিক তথ্য
BOT_TOKEN = '8967986442:AAFuDtXjhzyzhCFo_v--kjqoFym7atxmBIM'
GROUP_ID = '-1004204792339'

# === PythonAnywhere ফ্রি অ্যাকাউন্টের জন্য প্রক্সি সেটআপ ===
session = requests.Session()
session.proxies = {
    'http': 'http://proxy.server:3128',
    'https': 'http://proxy.server:3128',
}

# র্যান্ডম ওয়ালেট অ্যাড্রেস তৈরির ফাংশন (১০০% র্যান্ডম ক্যারেক্টার জেনারেট করবে)
def generate_random_wallet():
    # ক্রিপ্টো ওয়ালেটের জন্য (0-9 এবং a-f) ক্যারেক্টার নেওয়া হচ্ছে
    chars = '0123456789abcdef'
    part1 = ''.join(random.choices(chars, k=4)) # ৪টি র্যান্ডম অক্ষর/সংখ্যা
    part2 = ''.join(random.choices(chars, k=7)) # ৭টি র্যান্ডম অক্ষর/সংখ্যা
    return f"0x{part1}****{part2}"

def send_auto_message():
    while True:
        # ১. র্যান্ডম অ্যামাউন্ট জেনারেট (২০.০০ থেকে ১০০.০০ USDT)
        random_amount = round(random.uniform(20.00, 100.00), 2)
        amount_str = f"{random_amount:.2f} USDT"

        # ২. র্যান্ডম ওয়ালেট জেনারেট
        wallet_str = generate_random_wallet()

        # ৩. বর্তমান সময় ও তারিখ (টেলিগ্রাম ফরম্যাট অনুযায়ী)
        # যেমন: 7/9/2026, 12:15 PM
        current_time = datetime.now().strftime("%m/%d/%Y, %I:%M %p")

        # === আপনার মূল মেসেজ ফরম্যাট ===
        message = (
            "🟢 PAYMENT Complete 🟢\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"💵 Amount\n{amount_str}\n\n"
            "🌐 Network\nBNB Smart Chain (BEP-20)\n\n"
            f"👛 Recipient Wallet\n{wallet_str}\n\n\n"
            f"⏰ Processed\n{current_time}\n\n"
            "✅ Status\nCompleted Successfully\n"
            "━━━━━━━━━━━━━━━━━━"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': GROUP_ID,
            'text': message
        }

        try:
            # এখানে সাধারণ requests-এর বদলে প্রক্সি সেশন (session) ব্যবহার করা হয়েছে
            response = session.post(url, json=payload)
            if response.status_code == 200:
                print(f"[{current_time}] পেমেন্ট মেসেজ সফলভাবে পাঠানো হয়েছে। Amount: {amount_str}")
            else:
                print(f"টেলিগ্রাম সমস্যা: {response.text}")
        except Exception as e:
            print(f"প্রক্সি কানেকশন এরর: {e}")

        # ৩০ সেকেন্ড বিরতি
        time.sleep(30)

if __name__ == '__main__':
    print("প্রক্সি সাপোর্টসহ নতুন র্যান্ডম পেমেন্ট সিস্টেম চালু হচ্ছে...")
    send_auto_message()
