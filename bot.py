import requests
import re

# আপনার প্যানেলের সঠিক API Key এবং টেলিগ্রাম ইনফো
api_key = 'Sk_live_1x7jN6OUqTIzUNEv7MIM9Er2h5GphCXer9ef4BUx'
BOT_TOKEN = "8564093311:AAH55oqI6UmMfXycsEtxtIMjOHNN6atuVoo"
CHAT_ID = "-1003178872820"

# প্যানেলের আসল API লিংক
url = 'https://redxsms.com/api/v1/iprn/messages'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

params = {
    'type': 'a2p',
    'per_page': 10
}

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
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result.get("success") == True:
            messages = result.get("data", [])
            
            if messages:
                for item in messages:
                    source = item.get("source", "UNKNOWN")
                    number = str(item.get("number", ""))
                    msg_body = item.get("message", "")
                    status = item.get("status", "")
                    
                    otp_match = re.search(r'\b\d{4,6}\b', msg_body)
                    otp_code = otp_match.group(0) if otp_match else "N/A"
                    
                    formatted_msg = (
                        f"🔔 *New OTP Received*\n\n"
                        f"🏢 Source: `{source}`\n"
                        f"📱 Number: `{number}`\n"
                        f"💬 Message: `{msg_body}`\n"
                        f"📌 Status: `{status}`\n\n"
                        f"🔑 OTP: `{otp_code}`"
                    )
                    send_telegram_message(formatted_msg)
                print("Messages checked and sent successfully!")
            else:
                print("No messages found in data.")
        else:
            print("API returned success: false")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    check_messages()
