import telebot
from telebot import types
import requests
import socket
import time
import os
import random
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# የ Render ፖርት እና UptimeRobot (GET & HEAD) ጥያቄዎችን እንዲቀበል የተስተካከለ ሰርቨር
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

Thread(target=run_web).start()

# የቦትዎን ቶከን እዚህ ጋር ያስገቡ
TOKEN = "8788982436:AAHU8wHwD2Xt2FMOI4RaaLp_icb6Q-iCx9Y"

CHANNELS = ["@freeinternat10", "@Nur_Tunnel_free_ethiopian"]

bot = telebot.TeleBot(TOKEN)
user_states = {}

def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 1ኛ ቻናል ጆይን ለማድረግ", url="https://t.me/freeinternat10"))
        markup.add(types.InlineKeyboardButton("📢 2ኛ ቻናል ጆይን ለማድረግ", url="https://t.me/Nur_Tunnel_free_ethiopian"))
        markup.add(types.InlineKeyboardButton("✅ ጆይን አድርጌያለሁ (Check)", callback_data="check_join"))
        
        warning_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║    ⚠️ ቻናል ጆይን ማረጋገጫ    ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            "<b>ቦቱን ለመጠቀም እባክዎ በመጀመሪያ ሁለቱንም ቻናሎቻችንን ጆይን ያድርጉ!</b>\n\n"
            "1️⃣ @freeinternat10\n"
            "2️⃣ @Nur_Tunnel_free_ethiopian\n\n"
            "<i>ከተቀላቀሉ በኋላ ከታች ያለውን ቁልፍ ይጫኑ።</i>"
        )
        bot.send_message(message.chat.id, warning_msg, reply_markup=markup, parse_mode='HTML')
        return

    user_states[message.chat.id] = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🔑 SSH Account")
    btn2 = types.KeyboardButton("🚀 VLESS Config")
    btn3 = types.KeyboardButton("⚡ VMess Config")
    btn4 = types.KeyboardButton("🌐 VPNJantit Site")
    btn5 = types.KeyboardButton("🌐 FastSSH Site")
    btn6 = types.KeyboardButton("🔍 Host Scanner")
    btn7 = types.KeyboardButton("🌐 Subdomain Finder")
    btn8 = types.KeyboardButton("🌍 Zero-Rated Hosts")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    welcome_text = (
        "<b>╔═════════════════════════╗</b>\n"
        "<b>║   🤖 DYNAMIC SERVER BOT ║</b>\n"
        "<b>╚═════════════════════════╝</b>\n\n"
        "እንኳን ወደ ሰርቨር እና ኔትወርክ ማስተናገጃ ቦት በደህና መጡ።\n\n"
        "<i>እባክዎ ከታች ካሉት አዝራሮች የሚፈልጉትን አገልግሎት ይምረጡ፦</i>"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ እናመሰግናለን! ሁለቱንም ቻናሎች ጆይን አድርገዋል።")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        fake_message = call.message
        fake_message.text = "/start"
        send_welcome(fake_message)
    else:
        bot.answer_callback_query(call.id, "❌ አሁንም ሁለቱንም ቻናሎች ጆይን አላደረጉም! እባክዎ በመጀመሪያ ጆይን ይበሉ።", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 1ኛ ቻናል ጆይን ለማድረግ", url="https://t.me/freeinternat10"))
        markup.add(types.InlineKeyboardButton("📢 2ኛ ቻናል ጆይን ለማድረግ", url="https://t.me/Nur_Tunnel_free_ethiopian"))
        markup.add(types.InlineKeyboardButton("✅ ጆይን አድርጌያለሁ (Check)", callback_data="check_join"))
        bot.send_message(message.chat.id, "⚠️ ቦቱን ለመቀጠል እባክዎ ሁለቱንም ቻናሎች ጆይን ያድርጉ!", reply_markup=markup, parse_mode='HTML')
        return

    text = message.text.strip()
    chat_id = message.chat.id

    if text == "🚀 VLESS Config":
        user_states[chat_id] = None
        fallback_vless = [
            "vless://067fcd63-b215-4abd-8529-ae929a9971a9@145.239.55.210:443?encryption=auto&host=google.whatsapp.snapp.torob.basalam.fortresshost.ir.&path=/&security=tls&type=ws#🍂91@oneclickvpnkeys",
            "vless://067fcd63-b215-4abd-8529-ae929a9971a9@145.239.55.210:80?encryption=auto&host=google.whatsapp.snapp.torob.basalam.fortresshost.ir.&path=/&security=none&type=ws#🍂91@oneclickvpnkeys"
        ]
        selected_vless = random.choice(fallback_vless)
        result_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║   🚀 FREE VLESS CONFIG  ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            f"<code>{selected_vless}</code>"
        )
        bot.send_message(chat_id, result_msg, parse_mode='HTML')

    elif text == "⚡ VMess Config":
        user_states[chat_id] = None
        fallback_vmess = [
            "vmess://eyJhZGQiOiJ2bWVzcy1zZzEuc3Noa2l0Lm9yZyIsImFpZCI6IjAiLCJpZCI6ImU2MjBkNjAwLWVlMTktNDAxMi1hOTZjLTk2OGU4NWE1MmRlOSIsImhvc3QiOiJHb29nbGUuY29tIiwibmV0Ijoid3MiLCJwYXRoIjoiL3NzaGtpdC84NTc3NDUyODY0LzZhZDFjMmQ1OThiYTMvIiwicG9ydCI6IjgwIiwicHMiOiJ2bWVzcy1zZzEuc3Noa2l0Lm9yZyIsImRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==",
            "vmess://eyJhZGQiOiJ2bWVzcy1zZzEuc3Noa2l0Lm9yZyIsImFpZCI6IjAiLCJpZCI6ImU2MjBkNjAwLWVlMTktNDAxMi1hOTZjLTk2OGU4NWE1MmRlOSIsImhvc3QiOiJHb29nbGUuY29tIiwibmV0Ijoid3MiLCJwYXRoIjoiL3NzaGtpdC84NTc3NDUyODY0LzZhZDFjMmQ1OThiYTMvIiwicG9ydCI6IjQ0MyIsInBzIjoidm1lc3Mtc2cxLnNzaGtpdC5vcmciLCJ0bHMiOiJ0bHMiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0="
        ]
        selected_vmess = random.choice(fallback_vmess)
        result_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║   ⚡ FREE VMESS CONFIG  ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            f"<code>{selected_vmess}</code>"
        )
        bot.send_message(chat_id, result_msg, parse_mode='HTML')

    elif text == "🔑 SSH Account":
        user_states[chat_id] = None
        rand_num = random.randint(1000, 9999)
        ssh_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║   🔑 FREE SSH ACCOUNT   ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            f"🌐 <b>Host/IP:</b> <code>ssh.free-server-{rand_num}.com</code>\n"
            f"👤 <b>Username:</b> <code>user_{rand_num}</code>\n"
            f"🔐 <b>Password:</b> <code>pass{rand_num}</code>\n"
            "📌 <b>Ports:</b> <code>443 / 80 / 8080</code>\n\n"
            "<i>💡 (ይህ አካውንት በራሱ ጊዜ በዳይናሚክ የተፈጠረ ነው። በ HTTP Injector ወይም Dark Tunnel ይጠቀሙ)</i>"
        )
        bot.send_message(chat_id, ssh_msg, parse_mode='HTML')

    elif text == "🌐 VPNJantit Site":
        user_states[chat_id] = None
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 ወደ VPNJantit ዌብሳይት ለመሄድ", url="https://www.vpnjantit.com"))
        site_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║      🌐 VPNJANTIT       ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            "<i>ከታች ያለውን ቁልፍ በመጫን በራስዎ ፍላጎት ነፃ SSH ወይም V2Ray አካውንት መፍጠር ይችላሉ።</i>"
        )
        bot.send_message(chat_id, site_msg, reply_markup=markup, parse_mode='HTML')

    elif text == "🌐 FastSSH Site":
        user_states[chat_id] = None
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 ወደ FastSSH ዌብሳይት ለመሄድ", url="https://www.fastssh.com"))
        site_msg = (
            "<b>╔═════════════════════════╗</b>\n"
            "<b>║       🌐 FASTSSH        ║</b>\n"
            "<b>╚═════════════════════════╝</b>\n\n"
            "<i>ከታች ያለውን ቁልፍ በመጫን በራስዎ ፍላጎት ነፃ SSH ወይም VPN አካውንት መፍጠር ይችላሉ።</i>"
        )
        bot.send_message(chat_id, site_msg, reply_markup=markup, parse_mode='HTML')

    elif text == "🔍 Host Scanner":
        user_states[chat_id] = 'host_scanner'
        bot.send_message(chat_id, "<b>🔍 HOST SCANNER</b>\n\nእባክዎ መቃኘት የሚፈልጉትን ዶሜይን ወይም ሆስት በመጻፍ ይላኩ።", parse_mode='HTML')

    elif text == "🌐 Subdomain Finder":
        user_states[chat_id] = 'subdomain_finder'
        bot.send_message(chat_id, "<b>🌐 SUBDOMAIN FINDER</b>\n\nሰብ-ዶሜይን መፈለግ የሚፈልጉትን ዋና ዶሜይን በመጻፍ ይላኩ።", parse_mode='HTML')

    elif text == "🌍 Zero-Rated Hosts":
        user_states[chat_id] = 'zero_rated'
        bot.send_message(chat_id, "<b>🌍 ZERO-RATED HOSTS</b>\n\nእባክዎ የሚፈልጉትን ሀገር በመጻፍ ይላኩ።", parse_mode='HTML')

    else:
        state = user_states.get(chat_id)
        input_text = text.strip()

        if state == 'host_scanner':
            domain = input_text.replace("http://", "").replace("https://", "").split("/")[0]
            bot.send_message(chat_id, f"🛰️ <b>{domain}</b> ተቃኝቶ የተሻሻሉ ጥልቅ መረጃዎች እየመጡ ነው...", parse_mode='HTML')
            try:
                ip = socket.gethostbyname(domain)
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "N/A"
            except Exception:
                bot.send_message(chat_id, f"⚠️ <b>{domain}</b> IP አድራሻውን ማግኘት አልተቻለም።", parse_mode='HTML')
                return

            ports = [80, 443, 8080, 8443]
            result = (
                "<b>╔═════════════════════════╗</b>\n"
                "<b>║   🛡️ ADVANCED HOST SCAN ║</b>\n"
                "<b>╚═════════════════════════╝</b>\n\n"
                f"🎯 <b>Domain:</b> <code>{domain}</code>\n"
                f"📍 <b>IP Address:</b> <code>{ip}</code>\n"
                f"🏷️ <b>Reverse DNS:</b> <code>{hostname}</code>\n\n"
            )

            for port in ports:
                protocol = "https" if port in [443, 8443] else "http"
                url = f"{protocol}://{domain}:{port}"
                try:
                    start_time = time.time()
                    r = requests.get(url, timeout=6, allow_redirects=False)
                    latency = round((time.time() - start_time) * 1000)
                    status = r.status_code
                    server = r.headers.get('Server', 'Not disclosed')
                    
                    if status in [200, 403, 405]:
                        zero_rate = f"✅ Strong Bug Host (Status {status})"
                    elif status in [301, 302]:
                        zero_rate = f"⚠️ Redirect (Status {status})"
                    else:
                        zero_rate = f"❌ Unlikely (Status {status})"

                    result += f"🔹 <b>{protocol.upper()}:{port}</b> ➡️ ✅ <b>OPEN</b> ({latency}ms)\n"
                    result += f"   • Status: <b>{status}</b> | Bug: <b>{zero_rate}</b>\n"
                    result += f"   • Server: <code>{server}</code>\n\n"
                except Exception:
                    result += f"🔹 <b>{protocol.upper()}:{port}</b> ➡️ ❌ <b>Closed / Filtered</b>\n\n"

            bot.send_message(chat_id, result, parse_mode='HTML')

        elif state == 'subdomain_finder':
            domain = input_text.replace("http://", "").replace("https://", "").split("/")[0]
            bot.send_message(chat_id, f"🔍 ለ <b>{domain}</b> ሰብ-ዶሜይኖች በመሰብሰብ ላይ...", parse_mode='HTML')
            try:
                url = f"https://crt.sh/?q=%25.{domain}&output=json"
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    subdomains = set()
                    for entry in data:
                        for sub in entry.get('name_value', '').split('\n'):
                            sub = sub.strip()
                            if sub and '*' not in sub:
                                subdomains.add(sub)
                    sub_list = sorted(list(subdomains))
                    if sub_list:
                        if len(sub_list) > 20:
                            file_path = "subdomains.txt"
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write("\n".join(sub_list))
                            caption = f"🎯 <b>Target:</b> <code>{domain}</code>\n📊 <b>Total:</b> <code>{len(sub_list)}</code>\n<i>ቁጥራቸው ከ 20 ስለበለጠ በፋይል ተያይዟል!</i>"
                            with open(file_path, "rb") as doc:
                                bot.send_document(chat_id, doc, caption=caption, parse_mode='HTML')
                            try:
                                os.remove(file_path)
                            except:
                                pass
                        else:
                            result = f"🎯 <b>Target:</b> <code>{domain}</code>\n📊 <b>Total:</b> <code>{len(sub_list)}</code>\n\n"
                            for sub in sub_list:
                                result += f"🔹 <code>{sub}</code>\n"
                            bot.send_message(chat_id, result, parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, f"⚠️ ለ <b>{domain}</b> ምንም ሰብ-ዶሜይን ማግኘት አልተቻለም።", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, f"⚠️ ሰርቨሩ ምላሽ አልሰጠም፣ እንደገና ይሞክሩ።", parse_mode='HTML')
            except Exception:
                bot.send_message(chat_id, f"⚠️ የኔትወርክ ችግር አጋጥሟል።", parse_mode='HTML')

        elif state == 'zero_rated':
            country = input_text.lower()
            db = {
                "ethiopia": ["ethiotelecom.et", "safaricom.et", "telegram.org", "whatsapp.com"],
                "kenya": ["safaricom.co.ke", "airtel.co.ke", "whatsapp.com"],
                "global": ["telegram.org", "whatsapp.com", "cloudflare.com"]
            }
            hosts = db.get(country, ["telegram.org", "whatsapp.com", "cloudflare.com"])
            result = f"🌍 <b>Region:</b> <code>{input_text.capitalize()}</code>\n💡 <b>Verified Bug Hosts:</b>\n\n"
            for h in hosts:
                result += f"🔹 <code>{h}</code>\n"
            bot.send_message(chat_id, result, parse_mode='HTML')
        
        else:
            bot.send_message(chat_id, "⚠️ እባክዎ ከታች ካሉት አዝራሮች አገልግሎት ይምረጡ።", parse_mode='HTML')

if __name__ == '__main__':
    bot.infinity_polling()
