import requests
import re

# কনফিগারেশন
API_KEY = "sk_live_7ZMSGQEMA3DbtkmlnwrCNHjMuSroGrqkouQaoPag"
BOT_TOKEN = "8564093311:AAH55oqI6UmMfXycsEtxtIMjOHNN6atuVoo"
CHAT_ID = "-1003178872820"

BASE_URL = "https://ksiiprn.com/api/v1/iprn"

def get_country_flag(number):
    """নাম্বারের প্রিফিক্স দেখে কান্ট্রি ফ্ল্যাগ নির্ধারণ করার ফাংশশন"""
    if number.startswith("+964"):
        return "🇮🇶 Iraq"
    elif number.startswith("+1"):
        return "🇺🇸 USA"
    elif number.startswith("+44"):
        return "🇬🇧 UK"
    elif number.startswith("+880"):
        return "🇧🇩 Bangladesh"
    else:
        return "🌐 Unknown"

def detect_service(message_text):
    """মেসেজ থেকে সার্ভিস বা কোম্পানি ডিটেক্ট করার ফাংশশন"""
    text_upper = message_text.upper()
    if "WHATSAPP" in text_upper:
        return "💬 WhatsApp"
    elif "TELEGRAM" in text_upper:
        return "✈️ Telegram"
    elif "GOOGLE" in text_upper:
        return "🔍 Google"
    elif "FACEBOOK" in text_upper:
        return "📘 Facebook"
    else:
        return "🔔 OTP Service"

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

def check_messages():
    """প্যানেল থেকে মেসেজ ফেচ করে স্ক্রিনশটের স্টাইলে পাঠানোর ফাংশশন"""
    url = f"{BASE_URL}/messages"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get("success"):
            messages = result.get("data", [])
            for item in messages:
                number = item.get("number", "")
                msg_body = item.get("message", "")
                
                # মেসেজ থেকে ওটিপি কোড খুঁজে বের করা
                otp_match = re.search(r'\b\d{3}[- ]?\d{3}\b|\b\d{4,6}\b', msg_body)
                otp_code = otp_match.group(0) if otp_match else "N/A"
                
                flag_country = get_country_flag(number)
                service_name = detect_service(item.get("source", "") + " " + msg_body)
                
                # স্ক্রিনশটের স্টাইলে ফরম্যাট করা মেসেজ
                formatted_msg = (
                    f"{service_name} {flag_country} `{number}`\n\n"
                    f"`{msg_body}`\n\n"
                    f"🔍 Prefix : `{number[:5]}***`\n"
                    f"🔑 OTP : `{otp_code}`"
                )
                
                send_telegram_message(formatted_msg)
            print("Checked messages successfully!")
        else:
            print("API Error or No Data Found")
            
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    check_messages()
