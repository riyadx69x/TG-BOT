হা হা, ভাই একদম ঠিক ধরেছেন! এবার বুঝলাম প্যানেলের ডাটাতে সার্ভিস নেমের সাথে যে ছোট লাল ট্যাগটা থাকে ওটাই আসল ভেজাল করছিল। আপনার দেওয়া স্ক্রিনশটগুলোতে পরিষ্কার দেখা যাচ্ছে— প্রথম ছবিটিতে যেমন লেখা ছিল 1xBet A2P, এই কারণে আগের কোডগুলো ঘাবড়ে গিয়ে সার্ভিস নামটা ঠিকমতো ধরতে পারছিল না।
আপনার শেষ স্ক্রিনশটগুলোর (Telegram এবং WhatsApp ওয়ালা ডিজাইন) সাথে হুবহু মিল রেখে, প্যানেলের যেকোনো ডাটা (সেখানে A2P বা অন্য কিছু যাই থাকুক না কেন) থেকে একদম নিখুঁতভাবে সার্ভিস নেম, সঠিক কান্ট্রি ফ্ল্যাগ, মাস্কড নম্বর এবং টেলিগ্রামের ওই সুন্দর লুকটি এনে কোডটি আপডেট করে দিয়েছি।
নিচে একদম ফ্রেশ এবং ফুল কোডটি দিয়ে দিলাম, এটা সরাসরি কপি করে টার্মাকে বসিয়ে দিন:
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
    country_flags = {
        "93": "🇦🇫", "355": "🇦🇱", "213": "🇩🇿", "376": "🇦🇩", "244": "🇦🇴",
        "54": "🇦🇷", "374": "🇦🇲", "61": "🇦🇺", "43": "🇦🇹", "994": "🇦🇿",
        "973": "🇧🇭", "880": "🇧🇩", "375": "🇧🇾", "32": "🇧🇪", "501": "🇧🇿",
        "229": "🇧🇯", "975": "🇧🇹", "591": "🇧🇴", "387": "🇧🇦", "267": "🇧🇼",
        "55": "🇧🇷", "673": "🇧🇳", "359": "🇧🇬", "226": "🇧🇫", "257": "🇧🇮",
        "855": "🇰🇭", "237": "🇨🇲", "1": "🇺🇸", "238": "🇨🇻", "236": "🇨🇫",
        "235": "🇹🇩", "56": "🇨🇱", "86": "🇨🇳", "57": "🇨🇴", "269": "🇰🇲",
        "242": "🇨🇬", "243": "🇨🇩", "506": "🇨🇷", "385": "🇭🇷", "53": "🇨🇺",
        "357": "🇨🇾", "420": "🇨🇿", "45": "🇩🇰", "253": "🇩🇯", "1767": "🇩🇲",
        "1809": "🇩🇴", "593": "🇪🇨", "20": "🇪🇬", "503": "🇸🇻", "240": "🇬🇶",
        "291": "🇪🇷", "372": "🇪🇪", "251": "🇪🇹", "679": "🇫🇯", "358": "🇫🇮",
        "33": "🇫🇷", "241": "🇬🇦", "220": "🇬🇲", "995": "🇬🇪", "49": "🇩🇪",
        "233": "🇬🇭", "30": "🇬🇷", "502": "🇬🇹", "224": "🇬🇳", "245": "🇬🇼",
        "592": "🇬🇾", "509": "🇭🇹", "504": "🇭🇳", "36": "🇭🇺", "354": "🇮🇸",
        "91": "🇮🇳", "62": "🇮🇩", "98": "🇮🇷", "964": "🇮🇶", "353": "🇮🇪",
        "972": "🇮🇱", "39": "🇮🇹", "1876": "🇯🇲", "81": "🇯🇵", "962": "🇯🇴",
        "7": "🇰🇿", "254": "🇰🇪", "965": "🇰🇼", "996": "🇰🇬", "856": "🇱🇦",
        "371": "🇱🇻", "961": "🇱🇧", "266": "🇱🇸", "231": "🇱🇷", "218": "🇱🇾",
        "423": "🇱🇮", "370": "🇱🇹", "352": "🇱🇺", "261": "🇲🇬", "265": "🇲🇼",
        "60": "🇲🇾", "960": "🇲🇻", "223": "🇲🇱", "356": "🇲🇹", "52": "🇲🇽",
        "373": "🇲🇩", "377": "🇲🇨", "976": "🇲🇳", "382": "🇲🇪", "212": "🇲🇦",
        "258": "🇲🇿", "95": "🇲🇲", "264": "🇳🇦", "977": "🇳🇵", "31": "🇳🇱",
        "64": "🇳🇿", "505": "🇳🇮", "227": "🇳🇪", "234": "🇳🇬", "47": "🇳🇴",
        "968": "🇴🇲", "92": "🇵🇰", "970": "🇵🇸", "507": "🇵🇦", "675": "🇵🇬",
        "595": "🇵🇾", "51": "🇵🇪", "63": "🇵🇭", "48": "🇵🇱", "351": "🇵🇹",
        "974": "🇶🇦", "40": "🇷🇴", "7": "🇷🇺", "250": "🇷🇼", "966": "🇸🇦",
        "221": "🇸🇳", "381": "🇷🇸", "248": "🇸🇨", "232": "🇸🇱", "65": "🇸🇬",
        "421": "🇸🇰", "386": "🇸🇮", "252": "🇸🇴", "27": "🇿🇦", "82": "🇰🇷",
        "34": "🇪🇸", "94": "🇱🇰", "249": "🇸🇩", "597": "🇸🇷", "46": "🇸🇪",
        "41": "🇨🇭", "963": "🇸🇾", "886": "🇹🇼", "992": "🇹🇯", "255": "🇹🇿",
        "66": "🇹🇭", "228": "🇹🇬", "676": "🇹🇴", "216": "🇹🇳", "90": "🇹🇷",
        "993": "🇹🇲", "256": "🇺🇬", "380": "🇺🇦", "971": "🇦🇪", "44": "🇬🇧",
        "598": "🇺🇾", "998": "🇺🇿", "58": "🇻🇪", "84": "🇻🇳", "967": "🇾🇪",
        "260": "🇿🇲", "263": "🇿🇼"
    }
    
    for prefix_code in sorted(country_flags.keys(), key=len, reverse=True):
        if number.startswith(prefix_code):
            return country_flags[prefix_code]
    return "🌐"

def mask_number(number):
    # আপনার স্ক্রিনশটের মতো নম্বর মাস্কিং (যেমন: 88019****684 বা 26378****753)
    if len(number) > 8:
        return number[:5] + "****" + number[-3:]
    return number

def get_service_info(item, message_text):
    detected_name = ""
    
    # প্যানেলের বিভিন্ন ফিল্ড চেক করা এবং 'A2P' থাকলে তা বাদ দিয়ে আসল সার্ভিস নাম বের করা
    for key in ['service', 'app', 'service_name', 'name', 'title', 'gateway']:
        if key in item and item[key]:
            val = str(item[key]).strip()
            if val and val.lower() != "none":
                # যদি নামটির সাথে 'A2P' যুক্ত থাকে, তবে সেটা পরিষ্কার করে ফেলা
                val = val.replace("A2P", "").replace("a2p", "").strip()
                if val:
                    detected_name = val
                    break
                    
    # যদি উপরে না পাওয়া যায়, পুরো আইটেমের ভেতর খোঁজা
    if not detected_name:
        for key, value in item.items():
            if value and isinstance(value, str):
                val_lower = value.lower()
                for app in ["telegram", "whatsapp", "1xbet", "google", "facebook", "imo", "viber"]:
                    if app in val_lower:
                        detected_name = app.capitalize()
                        if app == "1xbet":
                            detected_name = "1xBet"
                        break
                if detected_name:
                    break

    # তাও না পেলে মেসেজ টেক্সট থেকে ডিটেক্ট করা
    if not detected_name or detected_name.lower() == "none":
        text_upper = message_text.upper()
        if "TELEGRAM" in text_upper:
            detected_name = "Telegram"
        elif "WHATSAPP" in text_upper:
            detected_name = "WhatsApp"
        elif "1XBET" in text_upper:
            detected_name = "1xBet"
        elif "GOOGLE" in text_upper:
            detected_name = "Google"
        else:
            detected_name = "Service"

    # সার্ভিস অনুযায়ী সঠিক ইমোজি সেট করা (আপনার স্ক্রিনশটের মতো হুবহু)
    s_upper = detected_name.upper()
    if "TELEGRAM" in s_upper:
        emoji = "✈️"
    elif "WHATSAPP" in s_upper:
        emoji = "💬"
    elif "1XBET" in s_upper:
        emoji = "🎰"
    elif "GOOGLE" in s_upper:
        emoji = "🌐"
    else:
        emoji = "💬"
        
    return detected_name, emoji

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
        params = {'per_page': 5}
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
                
                service_name, service_emoji = get_service_info(latest_item, msg_body)
                flag = get_country_flag(raw_number)
                masked_num = mask_number(raw_number)
                prefix = raw_number[:5] if len(raw_number) >= 5 else raw_number
                
                # আপনার স্ক্রিনশটের মতো ওটিপি বা কোড রিড করার রেজেক্স
                otp_match = re.search(r'\b\d{3}[-\s]?\d{3}\b|\b\d{4,6}\b', msg_body)
                otp_code = otp_match.group(0) if otp_match else "N/A"
                
                # আপনার স্ক্রিনশটের নিখুঁত আউটপুট ফরম্যাট
                formatted_msg = (
                    f"{service_emoji} {service_name} {flag} `{masked_num}`\n\n"
                    f"```{msg_body}```\n\n"
                    f"🔍 Prefix : `+{prefix}`\n"
                    f"🔑 OTP : `{otp_code}`\n\n"
                    f"{service_emoji} 📋 `{otp_code}`"
                )
                
                send_telegram_message(formatted_msg)
                save_last_processed_id(msg_id)
                print("OTP sent with perfect format!")
            else:
                print("No new messages.")
        else:
            print("No messages available.")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    check_messages()

