import requests
import re

# আপনার প্যানেলের API Key এবং টেলিগ্রাম ইনফো
api_key = 'Sk_live_1x7jN6OUqTIzUNEv7MIM9Er2h5GphCXer9ef4BUx'
BOT_TOKEN = "8564093311:AAH55oqI6UmMfXycsEtxtIMjOHNN6atuVoo"
CHAT_ID = "-1003178872820"

# সঠিক Base URL
url = 'https://redxsms.com/api/v1/iprn'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

def get_country_flag(number):
    """নাম্বারের প্রিফিক্স দেখে কান্ট্রি ফ্ল্যাগ নির্ধারণ"""
    if number.startswith("964"):
        return "🇮🇶"
    elif number.startswith("213"):
        return "🇩🇿"
    elif number.startswith("1"):
        return "🇺🇸"
    elif number.startswith("880"):
        return "🇧🇩"
    else:
        return "🌐"

def mask_number(number):
    """নাম্বারকে স্ক্রিনশটের মতো মাস্ক করা (যেমন: 96478****220)"""
    if len(number) > 7:
        return number[:5] + "****" + number[-3:]
    return number

def detect_service(message_text):
    """মেসেজ থেকে সার্ভিস ডিটেক্ট করা"""
    text_upper = message_text.upper()
    if "WHATSAPP BUSINESS" in text_upper:
        return "💬 WhatsApp Business"
    elif "WHATSAPP" in text_upper:
        return "💬 WhatsApp"
    elif "1XBET" in text_upper:
        return "🎲 1xBet"
    elif "TELEGRAM" in text_upper:
        return "✈️ Telegram"
    elif "GOOGLE" in text_upper:
        return "🔍 Google"
    else:
        return "🔔 A2P Service"

def send_telegram_message(text):
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(tg_url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_messages():
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get("success") == True:
            messages = result.get("data", []) or result.get("messages", [])
            
            if messages:
                for item in messages:
                    raw_number = str(item.get("number", ""))
                    msg_body = item.get("message", "") or item.get("text", "")
                    
                    # ওটিপি কোড খুঁজে বের করা (যেমন: 335-302 বা সাধারণ সংখ্যা)
                    otp_match = re.search(r'\b\d{3}[-\s]?\d{3}\b|\b\d{4,6}\b', msg_body)
                    otp_code = otp_match.group(0) if otp_match else "N/A"
                    # ওটিপির ভেতরের স্পেস বা হাইফেন স্ট্যান্ডার্ড করা চাইলে রাখতে পারেন
                    
                    flag = get_country_flag(raw_number)
                    masked_num = mask_number(raw_number)
                    service = detect_service(msg_body)
                    prefix = raw_number[:4] if len(raw_number) >= 4 else raw_number
                    
                    # স্ক্রিনশটের স্টাইলে ফরম্যাট তৈরি
                    formatted_msg = (
                        f"💬 {service} {flag} `{masked_num}`\n\n"
                        f"> {msg_body}\n\n"
                        f"🔍 Prefix : `+{prefix}`\n"
                        f"🔑 OTP : `{otp_code}`\n\n"
                        f"`💬 📋 {otp_code}`"
                    )
                    send_telegram_message(formatted_msg)
                print("Messages processed successfully!")
            else:
                print("No messages found right now.")
        else:
            print("API returned success: false.")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    check_messages()
