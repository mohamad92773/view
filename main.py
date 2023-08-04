import os
import telebot
import requests
from telebot import types
from threading import Thread
from time import sleep

token = "6491735739:AAHrcYJo7mACM3dWPPwZHG5ua7oM-JDn14M"
bot = telebot.TeleBot(token)

keys = [
    "d76cec185744253d84db4b49138e78a3",
    "46bffcfc73e280f50574fc49a7fbb01e",
    "8d0804c3c9ab8be16af4b7d6f40cf663",
    "b769dfff91e0dc7c358444cf4f6a88ff",
    "758c07e12fb5b0ceb7f5ae12c4daea5a",
    "4e0a9542ab299331dffbe87d44b119c4",
    "7690299527f7c38008974a063b78e2b7",
    "c959ae93ece6df681ca6f759baddce08",
    "e6fe16a552debd75dc0e8a7c5dfce1fa",
    "1b6263ff0035d7ff6106fbe7ad08e5c5",
    "dc17343f2bd64125dfd7f192c8a5dea4",
    "dbcec7233e2377d7a11bf5724d505c7c",
    "e4706a8667da68298346a110f1d89d7c",
    "aa2de25299aa945caf5ab5ef40bfbd27",
    "86d35d17a8d0384113f3f2561a1b4599",
    "3c627dcbbdd91684bd10101b40f65030",
    "1a6ad83b37dce75546b5dbe3a761da62",
    "f0414185d5e0caa4d0e77c712cbb6168",
    "bcb97cd8ab86852c934d5883b7dd0f66",
    "722fa8718c49af4576831ec9aa04171e",
    "4b6981c86ea73542b4320fb9632b6437",
    "3305da2b630689f87b9c57a6e0f68bcc",
    "626e92bb2c41a93c040219335ece4350",
    "63f59fde691e3eed67253873b1f04dea",
    "5d0b3f57c5f734f92e1a436e7d5e0f94"
]

current_key_index = 0
total_users = 0
users_set = set()
auto_rush_active = False

def get_order_status(api_key, order_id):
    url = f'https://smmgen.com/api/v2/?key={api_key}&action=status&order={order_id}'
    response = requests.get(url).json()
    return response

def get_total_links_rushed():
    total_links_rushed = 0
    return total_links_rushed

def is_user_subscribed(user_id):
    try:
        user = bot.get_chat_member("@redux_i", user_id)
        return user.status in ["member", "creator", "admin"]
    except Exception:
        return False

def notify_owner_on_new_user(user_id, username, name, total_users):
    owner_message = f"مستخدم جديد في البوت:\nالمعرف: @{username}\nالاسم: {name}\nالايدي: {user_id}\nعدد المستخدمين الكلي في البوت: {total_users}"
    bot.send_message("1167060300", owner_message)

@bot.message_handler(commands=['start'])
def start(message):
    global users_set, total_users
    chat_id = message.chat.id
    name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    if is_user_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="رشق تلقائي", callback_data='start_order_auto')
        button2 = types.InlineKeyboardButton(text="تحديثات", url="https://t.me/redux_i")
        button3 = types.InlineKeyboardButton(text="مساعدة", callback_data='help')
        markup.add(button1, button2)
        markup.add(button3)
        bot.send_message(chat_id, f"مرحبًا {name} بك في بوت Redux\nاختر ما تريده من الازرار\nDev : @redux_i.", reply_markup=markup)

        if user_id not in users_set:
            users_set.add(user_id)
            total_users += 1
            notify_owner_on_new_user(user_id, username, name, total_users)
    else:
        bot.send_message(chat_id, f"يجب أن تكون مشتركًا في قناة المالك @redux_i لاستخدام البوت. يرجى الاشتراك أولاً.")

@bot.callback_query_handler(func=lambda call: call.data == 'start_order_auto')
def start_order_auto(call):
    global auto_rush_active
    chat_id = call.message.chat.id
    auto_rush_active = True
    bot.send_message(chat_id, "يرجى إرسال رابط المنشور الذي ترغب في رشقه تلقائيًا.\nإذا كنت ترغب في إيقاف الرشق التلقائي، ارسل /stop_auto")

@bot.message_handler(commands=['stop_auto'])
def stop_auto(message):
    global auto_rush_active
    chat_id = message.chat.id
    auto_rush_active = False
    bot.send_message(chat_id, "تم إيقاف الرشق التلقائي.")

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_message(call):
    chat_id = call.message.chat.id
    help_text = """
    أهلاً بك في بوت Redux!
    يمكنك استخدام الأوامر التالية:
    /start - للبدء بعملية الرشق اليدوي.
    /stop_auto - لإيقاف عملية الرشق التلقائي.
    /stats - لعرض إحصائيات الرشق.
    """
    bot.send_message(chat_id, help_text)

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in users_set:
        users_set.remove(user_id)
        bot.send_message(chat_id, "تم إيقاف الرشق التلقائي.")
    else:
        bot.send_message(chat_id, "أنت لم تقم بتشغيل الرشق التلقائي بعد.")

@bot.message_handler(commands=['stats'])
def stats(message):
    chat_id = message.chat.id
    total_links_rushed = get_total_links_rushed()
    stats_message = f"عدد الروابط التي تم رشقها: {total_links_rushed}"
    bot.send_message(chat_id, stats_message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text

    if auto_rush_active and user_text.startswith('https://t.me'):
        bot.send_message(chat_id, "جاري معالجة الروابط...")
        if user_text.endswith('/'):
            user_text = user_text[:-1]

        links = user_text.split()
        current_thread = Thread(target=start_auto_rush, args=(chat_id, links))
        current_thread.start()
    else:
        bot.send_message(chat_id, "أنت غير مشترك في قناة المالك @redux_i. يرجى الاشتراك أولاً لاستخدام البوت.")

def start_auto_rush(chat_id, links):
    global current_key_index

    for link in links:
        while auto_rush_active:
            req = requests.get(f'https://smmgen.com/api/v2/?key={keys[current_key_index]}&action=add&service=9437&link={link}&quantity=1000').json()

            if "order" in req:
                order_id = req["order"]
                bot.send_message(chat_id, f"تم رشق الرابط بنجاح. رقم الطلب: {order_id}")
                sleep(33)
                current_key_index = (current_key_index + 1) % len(keys)
            elif "error" in req and "active order with this link" in req["error"]:
                bot.send_message(chat_id, "هذا الرابط مرتبط بطلب فعال. الرجاء الانتظار حتى اكتمال الطلب.")
                sleep(33)
                current_key_index = (current_key_index + 1) % len(keys)
            else:
                bot.send_message(chat_id, "حدث خطأ غير معروف.")
                break

def polling_thread():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")

polling_thread = Thread(target=polling_thread)
polling_thread.start()
while True:
    sleep(1) 
