import requests
import re
import os
import json
import time

api_key = 'sk_live_1x7jN6OUqTIzUNEv7MIM9Er2h5GphCXer9ef4BUx'
BOT_TOKEN = "8564093311:AAE1wtnRDybV4oOH3HgmJbHplsBovYVtZm8"
CHAT_ID = "-1003178872820"

url = 'https://redxsms.com/api/v1/iprn/messages'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

LAST_ID_FILE = "last_id.txt"

def get_country_code_and_flag(number):
    country_data = {
        "93": ("AF", "🇦🇫"), "355": ("AL", "🇦🇱"), "213": ("DZ", "🇩🇿"), "376": ("AD", "🇦🇩"), "244": ("AO", "🇦🇴"),
        "54": ("AR", "🇦🇷"), "374": ("AM", "🇦🇲"), "61": ("AU", "🇦🇺"), "43": ("AT", "🇦🇹"), "994": ("AZ", "🇦🇿"),
        "973": ("BH", "🇧🇭"), "880": ("BD", "🇧🇩"), "375": ("BY", "🇧🇾"), "32": ("BE", "🇧🇪"), "501": ("BZ", "🇧🇿"),
        "229": ("BJ", "🇧🇯"), "975": ("BT", "🇧🇹"), "591": ("BO", "🇧🇴"), "387": ("BA", "🇧🇦"), "267": ("BW", "🇧🇼"),
        "55": ("BR", "🇧🇷"), "673": ("BN", "🇧🇳"), "359": ("BG", "🇧🇬"), "226": ("BF", "🇧🇫"), "257": ("BI", "🇧🇮"),
        "855": ("KH", "🇰🇭"), "237": ("CM", "🇨🇲"), "1": ("US", "🇺🇸"), "238": ("CV", "🇨🇻"), "236": ("CF", "🇨🇫"),
        "235": ("TD", "🇹🇩"), "56": ("CL", "🇨🇱"), "86": ("CN", "🇨🇳"), "57": ("CO", "🇨🇴"), "269": ("KM", "🇰🇲"),
        "242": ("CG", "🇨🇬"), "243": ("CD", "🇨🇩"), "506": ("CR", "🇨🇷"), "385": ("HR", "🇭🇷"), "53": ("CU", "🇨🇺"),
        "357": ("CY", "🇨🇾"), "420": ("CZ", "🇨🇿"), "45": ("DK", "🇩🇰"), "253": ("DJ", "🇩🇯"), "1767": ("DM", "🇨🇲"),
        "1809": ("DO", "🇩🇴"), "593": ("EC", "🇪🇨"), "20": ("EG", "🇪🇬"), "503": ("SV", "🇸🇻"), "240": ("GQ", "🇬🇶"),
        "291": ("ER", "🇪🇷"), "372": ("EE", "🇪🇪"), "251": ("ET", "🇪🇹"), "679": ("FJ", "🇫🇯"), "358": ("FI", "🇫🇮"),
        "33": ("FR", "🇫🇷"), "241": ("GA", "🇬🇦"), "220": ("GM", "🇬🇲"), "995": ("GE", "🇬🇪"), "49": ("DE", "🇩🇪"),
        "233": ("GH", "🇬🇭"), "30": ("GR", "🇬🇷"), "502": ("GT", "🇬🇹"), "224": ("GN", "🇬🇳"), "245": ("GW", "🇬🇼"),
        "592": ("GY", "🇬🇾"), "509": ("HT", "🇭🇹"), "504": ("HN", "🇭🇳"), "36": ("HU", "🇭🇺"), "354": ("IS", "🇮🇸"),
        "91": ("IN", "🇮🇳"), "62": ("ID", "🇮🇩"), "98": ("IR", "🇮🇷"), "964": ("IQ", "🇮🇶"), "353": ("IE", "🇮🇪"),
        "972": ("IL", "🇮🇱"), "39": ("IT", "🇮🇹"), "1876": ("JM", "🇯🇲"), "81": ("JP", "🇯🇵"), "962": ("JO", "🇯🇴"),
        "7": ("KZ", "🇰🇿"), "254": ("KE", "🇰🇪"), "965": ("KW", "🇰🇼"), "996": ("KG", "🇰🇬"), "856": ("LA", "🇱🇦"),
        "371": ("LV", "🇱🇻"), "961": ("LB", "🇱🇧"), "266": ("LS", "🇱🇸"), "231": ("LR", "🇱🇷"), "218": ("LY", "🇱🇾"),
        "423": ("LI", "🇱🇮"), "370": ("LT", "🇱🇹"), "352": ("LU", "🇱🇺"), "261": ("MG", "🇲🇬"), "265": ("MW", "🇲🇼"),
        "60": ("MY", "🇲🇾"), "960": ("MV", "🇲🇻"), "223": ("ML", "🇲🇱"), "356": ("MT", "🇲🇹"), "52": ("MX", "🇲🇽"),
        "373": ("MD", "🇲🇩"), "377": ("MC", "🇲🇨"), "976": ("MN", "🇲🇳"), "382": ("ME", "🇲🇪"), "212": ("MA", "🇲🇦"),
        "258": ("MZ", "🇲🇿"), "95": ("MM", "🇲🇲"), "264": ("NA", "🇳🇦"), "977": ("NP", "🇳🇵"), "31": ("NL", "🇳🇱"),
        "64": ("NZ", "🇳🇿"), "505": ("NI", "🇳🇮"), "227": ("NE", "🇳🇪"), "234": ("NG", "🇳🇬"), "47": ("NO", "🇳🇴"),
        "968": ("OM", "🇴🇲"), "92": ("PK", "🇵🇰"), "970": ("PS", "🇵🇸"), "507": ("PA", "🇵🇦"), "675": ("PG", "🇵🇬"),
        "595": ("PY", "🇵🇾"), "51": ("PE", "🇵🇪"), "63": ("PH", "🇵🇭"), "48": ("PL", "🇵🇱"), "351": ("PT", "🇵🇹"),
        "974": ("QA", "🇶🇦"), "40": ("RO", "🇷🇴"), "7": ("RU", "🇷🇺"), "250": ("RW", "🇷🇼"), "966": ("SA", "🇸🇦"),
        "221": ("SN", "🇸🇳"), "381": ("RS", "🇷🇸"), "248": ("SC", "🇸🇨"), "232": ("SL", "🇸🇱"), "65": ("SG", "🇸🇬"),
        "421": ("SK", "🇸🇰"), "386": ("SI", "🇸🇮"), "252": ("SO", "🇸🇴"), "27": ("ZA", "🇿🇦"), "82": ("KR", "🇰🇷"),
        "34": ("ES", "🇪🇸"), "94": ("LK", "🇱🇰"), "249": ("SD", "🇸🇩"), "597": ("SR", "🇸🇷"), "46": ("SE", "🇸🇪"),
        "41": ("CH", "🇨🇭"), "963": ("SY", "🇸🇾"), "886": ("TW", "🇹🇼"), "992": ("TJ", "🇹🇯"), "255": ("TZ", "🇹🇿"),
        "66": ("TH", "🇹🇭"), "228": ("TG", "TG"), "676": ("TO", "🇹🇴"), "216": ("TN", "🇹🇳"), "90": ("TR", "🇹🇷"),
        "993": ("TM", "🇹🇲"), "256": ("UG", "🇺🇬"), "380": ("UA", "🇺🇦"), "971": ("AE", "🇦🇪"), "44": ("GB", "🇬🇧"),
        "598": ("UY", "🇺🇾"), "998": ("UZ", "🇺🇿"), "58": ("VE", "🇻🇪"), "84": ("VN", "🇻🇳"), "967": ("YE", "🇾🇪"),
        "260": ("ZM", "🇿🇲"), "263": ("ZW", "🇿🇼")
    }
    
    for prefix_code in sorted(country_data.keys(), key=len, reverse=True):
        if number.startswith(prefix_code):
            return country_data[prefix_code]
    return "GEN", "🌐"

def mask_phone_number(number):
    if len(number) > 6:
        return number[:3] + "Error" + number[6:]
    return number

def get_service_info(item, message_text):
    detected_name = ""
    for key in ['service', 'app', 'service_name', 'name', 'title', 'gateway']:
        if key in item and item[key]:
            val = str(item[key]).strip()
            if val and val.lower() != "none":
                detected_name = val
                break
                
    if not detected_name:
        text_upper = message_text.upper()
        if "TELEGRAM" in text_upper:
            detected_name = "Telegram"
        elif "WHATSAPP" in text_upper:
            detected_name = "WhatsApp"
        elif "1XBET" in text_upper:
            detected_name = "1xBet"
        elif "GOOGLE" in text_upper:
            detected_name = "Google"
        elif "FACEBOOK" in text_upper:
            detected_name = "Facebook"
        else:
            detected_name = "OTP"

    s_upper = detected_name.upper()
    if "TELEGRAM" in s_upper:
        emoji = "📱"
    elif "WHATSAPP" in s_upper:
        emoji = "💬"
    else:
        emoji = ""
        
    return emoji, detected_name

def send_telegram_message(text, emoji, otp_code):
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": f"{emoji}  {otp_code}",
                    "copy_text": {"text": otp_code}
                },
                {
                    "text": " Number Bot ",
                    "url": "https://t.me/Worldfast_otpxbot"
                }
            ]
        ]
    }
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(inline_keyboard)
    }
    try:
        response = requests.post(tg_url, json=payload, timeout=10)
        res_data = response.json()
        if res_data.get("ok"):
            message_id = res_data["result"]["message_id"]
            save_message_for_deletion(message_id)
    except Exception as e:
        print(f"Telegram Error: {e}")

DELETION_FILE = "pending_deletions.json"

def save_message_for_deletion(message_id):
    current_time = time.time()
    data = []
    if os.path.exists(DELETION_FILE):
        try:
            with open(DELETION_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []
    data.append({"message_id": message_id, "delete_at": current_time + 300})
    with open(DELETION_FILE, "w") as f:
        json.dump(data, f)

def check_pending_deletions():
    if not os.path.exists(DELETION_FILE):
        return
    try:
        with open(DELETION_FILE, "r") as f:
            data = json.load(f)
    except:
        return
    
    current_time = time.time()
    remaining = []
    for item in data:
        if current_time >= item["delete_at"]:
            del_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
            try:
                requests.post(del_url, json={"chat_id": CHAT_ID, "message_id": item["message_id"]}, timeout=10)
            except Exception as e:
                print(f"Delete Error: {e}")
        else:
            remaining.append(item)
            
    with open(DELETION_FILE, "w") as f:
        json.dump(remaining, f)

if os.path.exists(LAST_ID_FILE):
    os.remove(LAST_ID_FILE)

def check_messages():
    try:
        params = {'per_page': 50}
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        if response.status_code != 200:
            return
            
        result = response.json()
        messages = result.get("data", [])
        
        if messages:
            messages.reverse()
            
            sent_ids = set()
            if os.path.exists("sent_messages.json"):
                with open("sent_messages.json", "r") as f:
                    try:
                        sent_ids = set(json.load(f))
                    except:
                        sent_ids = set()

            new_sent = False
            for latest_item in messages:
                msg_id = str(latest_item.get("id", latest_item.get("received_at", "")))
                
                if msg_id not in sent_ids:
                    raw_number = str(latest_item.get("number", ""))
                    msg_body = latest_item.get("message", "")
                    
                    service_emoji, service_name = get_service_info(latest_item, msg_body)
                    country_short, flag = get_country_code_and_flag(raw_number)
                    prefix = raw_number[:9] if len(raw_number) >= 9 else raw_number
                    
                    masked_number = mask_phone_number(raw_number)
                    
                    otp_match = re.search(r'\b\d{3}[-\s]?\d{3}\b|\b\d{4,6}\b', msg_body)
                    otp_code = otp_match.group(0) if otp_match else "N/A"
                    
                    # Language detection
                    lang_name = "English"
                    if any(c in msg_body for c in "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯабвгдежзиклмнопрстуфхцчшщэюя"):
                        lang_name = "Russian"
                    elif any(c in msg_body for c in "ñáéíóú¿¡"):
                        lang_name = "Spanish"
                    elif any(c in msg_body for c in "äöüß"):
                        lang_name = "German"

                    # দেশের শর্ট নেম সঠিকভাবে এক লাইনে যুক্ত করা হলো
                    formatted_msg = (
                        f"╭─────────────────╮\n"
                        f"│{flag} {service_name} | {country_short} | `{masked_number}` | {lang_name} |\n"
                        f"│✨ Prefix: `{prefix}`\n"
                        f"╰─────────────────╯"
                    )
                    
                    send_telegram_message(formatted_msg, service_emoji, otp_code)
                    sent_ids.add(msg_id)
                    new_sent = True
                    time.sleep(0.05)
            
            if new_sent:
                with open("sent_messages.json", "w") as f:
                    json.dump(list(sent_ids), f)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Bot is running in Turbo Mode...")
    while True:
        check_messages()
        check_pending_deletions()
