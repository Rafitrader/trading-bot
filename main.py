import time
import requests
import pandas as pd

BOT_TOKEN = '8988002388:AAGrLEM2AbM9VjQvTSyjMAwnIJlUIHKKgZQ'
GROUP_ID = '-1003879489231'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': GROUP_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def get_binance_gold_candles():
    url = "https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval=1m&limit=5"
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
        print(f"Binance Fetch Error: {e}")
    return None

def start_real_signal_bot():
    print("🚀 Render ক্লাউড সার্ভার থেকে বট চালু হচ্ছে...")
    send_telegram_message("📡 *RENDER CLOUD BOT:* বট সফলভাবে রেন্ডার ক্লাউড থেকে চালু হয়েছে! ১ মিনিটের আসল গোল্ড ক্যান্ডেল স্ক্যান শুরু হলো...")
    
    active_trade = None
    last_processed_time = None
    
    while True:
        df = get_binance_gold_candles()
        if df is not None and len(df) >= 3:
            c1 = df.iloc[-2]
            c2 = df.iloc[-3]
            candle_time = int(c1['timestamp'])
            
            c1_green = c1['close'] > c1['open']
            c2_green = c2['close'] > c2['open']
            c1_red = c1['close'] < c1['open']
            c2_red = c2['close'] < c2['open']
            live_price = float(df.iloc[-1]['close'])
            
            if active_trade is None and candle_time != last_processed_time:
                decision = None
                if c1_green and c2_green: decision = "🟢 BUY"
                elif c1_red and c2_red: decision = "🔴 SELL"
                    
                if decision:
                    entry = live_price
                    tp = entry + 0.60 if decision == "🟢 BUY" else entry - 0.60
                    sl = entry - 0.60 if decision == "🟢 BUY" else entry + 0.60
                    
                    msg = (
                        f"📡 *NEW FOREX SMART SIGNAL (REAL)* 📡\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"💱 *Pair:* GOLD/USD (1 Min Chart)\n"
                        f"👉 *Action:* {decision}\n"
                        f"📌 *Entry Price:* {entry:.2f}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎯 *Take Profit Target:* \n"
                        f"   🔹 TP-1: {tp:.2f} (~6 Pips)\n\n"
                        f"🛑 *Stop Loss (SL):* {sl:.2f} (6 Pips)\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🤖 _Render ক্লাউড সার্ভার দ্বারা চালিত ২৪/৭ লাইভ আসল সিগন্যাল।_"
                    )
                    send_telegram_message(msg)
                    active_trade = {'dir': decision, 'entry': entry, 'tp': tp, 'sl': sl}
                    last_processed_time = candle_time
            
            elif active_trade:
                if active_trade['dir'] == "🟢 BUY":
                    if live_price >= active_trade['tp']:
                        send_telegram_message(f"Allhumdullah 📊😎\n\n💱 *Pair:* GOLD/USD\n🔹 *TP-1:* {active_trade['tp']:.2f} *TARGET HIT* ✅")
                        active_trade = None
                    elif live_price <= active_trade['sl']:
                        send_telegram_message(f"🛑 *STOP LOSS HIT* 🔴\n\n💱 *Pair:* GOLD/USD\n🛑 *SL:* {active_trade['sl']:.2f}")
                        active_trade = None
                elif active_trade['dir'] == "🔴 SELL":
                    if live_price <= active_trade['tp']:
                        send_telegram_message(f"Allhumdullah 📊😎\n\n💱 *Pair:* GOLD/USD\n🔹 *TP-1:* {active_trade['tp']:.2f} *TARGET HIT* ✅")
                        active_trade = None
                    elif live_price >= active_trade['sl']:
                        send_telegram_message(f"🛑 *STOP LOSS HIT* 🔴\n\n💱 *Pair:* GOLD/USD\n🛑 *SL:* {active_trade['sl']:.2f}")
                        active_trade = None
                        
        time.sleep(20)

if __name__ == '__main__':
    start_real_signal_bot()
