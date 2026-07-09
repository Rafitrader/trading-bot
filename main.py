import time
import requests
import pandas as pd
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# টেলিগ্রাম কনফিগারেশন
BOT_TOKEN = '8988002388:AAGrLEM2AbM9VjQvTSyjMAwnIJlUIHKKgZQ'
GROUP_ID = '-1003879489231'

# Render Web Service পোর্ট বাইন্ডিং ফিক্স করার ডামি সার্ভার
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Trading Bot is Running Perfectly!")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyServer)
    server.serve_forever()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': GROUP_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_binance_candles(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=5"
    try:
        response = requests.get(url, timeout=10).json()
        if isinstance(response, list) and len(response) > 0:
            candles = []
            for item in response:
                candles.append({
                    'timestamp': item[0],
                    'open': float(item[1]),
                    'high': float(item[2]),
                    'low': float(item[3]),
                    'close': float(item[4])
                })
            return pd.DataFrame(candles)
    except Exception as e:
        print(f"Binance Error for {symbol}: {e}")
    return None

def start_multi_market_bot():
    print("🚀 Render ক্লাউড থেকে মাল্টি-মার্কেট বট সফলভাবে চালু হয়েছে...")
    send_telegram_message("📡 *RENDER MULTI-BOT:* সফলভাবে বট চালু হয়েছে!\n📊 *Markets:* BTC/USDT & GOLD/USD (1 Min Chart)")
    
    # দুটি মার্কেটের জন্য আলাদা আলাদা ট্রেড ও টাইম ট্র্যাকিং স্টেট
    states = {
        'BTCUSDT': {'active_trade': None, 'last_time': None, 'tp_pips': 60.0, 'sl_pips': 60.0, 'name': 'BTC/USDT'},
        'PAXGUSDT': {'active_trade': None, 'last_time': None, 'tp_pips': 0.70, 'sl_pips': 0.70, 'name': 'GOLD/USD'}
    }
    
    while True:
        for symbol, state in states.items():
            df = get_binance_candles(symbol)
            if df is not None and len(df) >= 3:
                c1 = df.iloc[-2]  # ঠিক আগের ক্লোজ হওয়া ক্যান্ডেল
                c2 = df.iloc[-3]  # তার আগের ক্যান্ডেল
                candle_time = int(c1['timestamp'])
                live_price = float(df.iloc[-1]['close'])
                
                c1_green = c1['close'] > c1['open']
                c1_red = c1['close'] < c1['open']
                c2_green = c2['close'] > c2['open']
                c2_red = c2['close'] < c2['open']
                
                # নতুন সিগন্যাল চেকিং লজিক
                if state['active_trade'] is None and candle_time != state['last_time']:
                    decision = None
                    if c1_green and c2_green: decision = "🟢 BUY"
                    elif c1_red and c2_red: decision = "🔴 SELL"
                        
                    if decision:
                        entry = live_price
                        tp = entry + state['tp_pips'] if decision == "🟢 BUY" else entry - state['tp_pips']
                        sl = entry - state['sl_pips'] if decision == "🟢 BUY" else entry + state['sl_pips']
                        
                        msg = (
                            f"📡 *NEW FOREX/CRYPTO SMART SIGNAL* 📡\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"💱 *Pair:* {state['name']} (1 Min Chart)\n"
                            f"👉 *Action:* {decision}\n"
                            f"📌 *Entry Price:* {entry:.2f}\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"🎯 *Take Profit Target:* {tp:.2f}\n"
                            f"🛑 *Stop Loss (SL):* {sl:.2f}\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"🤖 _Render ক্লাউড সার্ভার দ্বারা চালিত ২৪/৭ লাইভ অটো সিগন্যাল।_"
                        )
                        send_telegram_message(msg)
                        state['active_trade'] = {'dir': decision, 'entry': entry, 'tp': tp, 'sl': sl}
                        state['last_time'] = candle_time
                
                # রানিং ট্রেডের প্রফিট/লস বা টার্গেট হিট চেকিং লজিক
                elif state['active_trade']:
                    trade = state['active_trade']
                    if trade['dir'] == "🟢 BUY":
                        if live_price >= trade['tp']:
                            send_telegram_message(f"Alhamdulillah 📊😎\n\n💱 *Pair:* {state['name']}\n🔹 *Target:* {trade['tp']:.2f} *TARGET HIT* ✅")
                            state['active_trade'] = None
                        elif live_price <= trade['sl']:
                            send_telegram_message(f"🛑 *STOP LOSS HIT* 🔴\n\n💱 *Pair:* {state['name']}\n🛑 *SL:* {trade['sl']:.2f}")
                            state['active_trade'] = None
                    elif trade['dir'] == "🔴 SELL":
                        if live_price <= trade['tp']:
                            send_telegram_message(f"Alhamdulillah 📊😎\n\n💱 *Pair:* {state['name']}\n🔹 *Target:* {trade['tp']:.2f} *TARGET HIT* ✅")
                            state['active_trade'] = None
                        elif live_price >= trade['sl']:
                            send_telegram_message(f"🛑 *STOP LOSS HIT* 🔴\n\n💱 *Pair:* {state['name']}\n🛑 *SL:* {trade['sl']:.2f}")
                            state['active_trade'] = None
                            
        time.sleep(10)  # প্রতি ১০ সেকেন্ডে দুই মার্কেট স্ক্যান করবে দ্রুত রেসপন্সের জন্য

if __name__ == '__main__':
    # Render-এর পোর্ট ফিক্স করার জন্য ব্যাকগ্রাউন্ড থ্রেড
    Thread(target=run_dummy_server, daemon=True).start()
    # আসল বট ইঞ্জিন স্টার্ট
    start_multi_market_bot()
