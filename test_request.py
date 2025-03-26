import telebot

TOKEN = "7546123349:AAFtcKsIvwpaBmyuApsxRos1yxzf_qrlf2k"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, message.chat.id)


bot.polling(none_stop=True)
