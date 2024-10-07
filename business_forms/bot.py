import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse(status=200)


class Handler:
    bot = bot

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'hello world')
