import requests
import re
import os

api_key = 'sk_live_1x7jN6OUqTIzUNEv7MIM9Er2h5GphCXer9ef4BUx'
BOT_TOKEN = "8564093311:AAH55oqI6UmMfXycsEtxtIMjOHNN6atuVoo"
CHAT_ID = "-1003178872820"

url = 'https://redxsms.com/api/v1/iprn/messages'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

LAST_ID_FILE = "last_id.txt"

def get_last_processed_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_processed_id(msg_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(msg_id))

def get_country_flag(number):
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
    if len(number) > 7:
        return number[:5] + "****" + number[-3:]
    return number

def detect_service(message_text):
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
        params = {'per_page': 10}
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        messages = result.get("data", [])
        
        if messages:
            latest_item = messages[0]
            msg_id = str(latest_item.get("id", latest_item.get("received_at", "")))
            
            last_saved_id = get_last_processed_id()
            
            if msg_id != last_saved_id:
                raw_number = str(latest_item.get("number", ""))
                msg_body = latest_item.get("message", "")
                
                otp_match = re.search(r'\b\d{3}[-\s]?\d{3}\b|\b\d{4,6}\b', msg_body)
                otp_code = otp_match.group(0) if otp_match else "N/A"
                
                flag = get_country_flag(raw_number)
                masked_num = mask_number(raw_number)
                service = detect_service(msg_body)
                prefix = raw_number[:4] if len(raw_number) >= 4 else raw_number
                
                formatted_msg = (
                    f"💬 {service} {flag} `{masked_num}`\n\n"
                    f"> {msg_body}\n\n"
                    f"🔍 Prefix : `+{prefix}`\n"
                    f"🔑 OTP : `{otp_code}`\n\n"
                    f"`💬 📋 {otp_code}`"
                )
                send_telegram_message(formatted_msg)
                save_last_processed_id(msg_id)
                print("New OTP sent to Telegram!")
            else:
                print("No new messages.")
        else:
            print("No messages available in panel.")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    check_messages()
