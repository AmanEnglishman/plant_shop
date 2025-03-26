# import telebot
#
# from .models import Checkout
#
# bot_token = '7130510261:AAEWidIK9jjtC70jN1YhGts7Ph57hD0rGBE'
# chat_id = '5249187638'
#
#
# def send_checkout(instance):
#     instance = Checkout.objects.all()
#     bot = telebot.TeleBot(bot_token)
#     message_text = (f"ФИО: {instance.first_name}\n"
#                 f"Номер: {number}\n"
#                 f"Текст отзыва: {text}")
#
#     bot.send_message(chat_id, message_text)
