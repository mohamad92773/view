import os
import telebot

# استخراج توكن البوت من متغير البيئة على Heroku
TOKEN = os.environ.get('TOKEN')

# إنشاء كائن البوت باستخدام التوكن
bot = telebot.TeleBot(TOKEN)

# تعريف الأوامر والاستجابات هنا
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحبًا بك! أنا هنا لمساعدتك.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# بدء تشغيل البوت
bot.polling()
