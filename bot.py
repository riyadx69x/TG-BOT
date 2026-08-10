import requests
import re

# আপনার নতুন ইনফরমেশন
API_KEY = "sk_live_7ZMSGQEMA3DbtkmlnwrCNHjMuSroGrqkouQaoPag"
BOT_TOKEN = "8564093311:AAH55oqI6UmMfXycsEtxtIMjOHNN6atuVoo"
CHAT_ID = "-1003178872820"

# আপনার দেওয়া প্যানেলের সঠিক API বেস লিংক
BASE_URL = "https://redxsms.com/Switchfy/api/v1"

def get_country_flag(number):
    """নাম্বারের প্রিফিক্স দেখে কান্ট্রি ফ্ল্যাগ নির্ধারণ করার ফাংশশন"""
    if number.startswith("213"):  # আলজেরিয়া (স্ক্রিনশট অনুযায়ী)
        return "🇩🇿 Algeria"
    elif number.startswith("+964") or number.startswith("964"):
        return "🇮🇶 Iraq"
    elif number.startswith("+1") or number.startswith("1"):
        return "🇺🇸 USA"
    elif number.startswith("+880") or number.startswith("880"):
        return "🇧🇩 Bangladesh"
    else:
        return "🌐 International"

def detect_service(message_text):
    """মেসেজ থেকে সার্ভিস বা কোম্পানি ডিটেক্ট করার ফাংশশন"""
    text_upper = message_text.upper()
    if "1XBET" in text_upper:
        return "🎲 1xBet"
    elif "WHATSAPP" in text_upper:
        return "💬 WhatsApp"
    elif "TELEGRAM" in text_upper:
        return "✈️ Telegram"
    elif "GOOGLE" in text_upper:
        return "🔍 Google"
    elif "FACEBOOK" in text_upper:
        return "📘 Facebook"
    else:
        return "🔔 A2P Service"

def send_telegram_message(text):
    """টেলিগ্রাম গ্রুপে মেসেজ পাঠানোর ফাংশশন"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_live_sms():
    """প্যানেলের লাইভ এসএমএস ফেচ করে সাজিয়ে পাঠানোর ফাংশশন"""
    url = f"{BASE_URL}/live-sms"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        
        # প্যানেলের রেসপন্স অনুযায়ী ডাটা প্রসেস করা
        messages = result.get("data", []) or result.get("messages", [])
        
        if messages:
            for item in messages:
                number = str(item.get("number", ""))
                msg_body = item.get("message", "") or item.get("text", "")
                
                # মেসেজ থেকে ওটিপি কোড খুঁজে বের করা (যেমন স্ক্রিনশটে থাকা 29957)
                otp_match = re.search(r'\b\d{4,6}\b', msg_body)
                otp_code = otp_match.group(0) if otp_match else "N/A"
                
                flag_country = get_country_flag(number)
                service_name = detect_service(msg_body)
                
                # আপনার চাওয়া স্টাইলে ফরম্যাট করা মেসেজ
                formatted_msg = (
                    f"{service_name} {flag_country} `{number}`\n\n"
                    f"`{msg_body}`\n\n"
                    f"🔍 Prefix : `+{number[:4]}`\n"
                    f"🔑 OTP : `{otp_code}`"
                )
                
                send_telegram_message(formatted_msg)
            print("Live SMS checked and sent successfully!")
        else:
            print("No live SMS found.")
            
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    check_live_sms()
