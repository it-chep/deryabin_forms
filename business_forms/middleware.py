import traceback
from django.conf import settings
from business_forms.bot import bot


class TelegramAlertMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            self.send_telegram_alert(request, response)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Exception) and not settings.DEBUG:
            self.send_telegram_alert(request, exception)
        return None

    def send_telegram_alert(self, request, exception):
        try:
            error_message = ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
            exception_type = type(exception).__name__
        except Exception:
            return

        message = (
            f"🚨 *500 Internal Server Error*\n"
            f"URL: {request.build_absolute_uri()}\n"
            f"Method: {request.method}\n"
            f"Status Code: 500\n"
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'}\n"
            f"Exception: {exception_type}\n"
            f"Error Message:\n```\n{error_message}\n```"
        )

        self.send_message_to_telegram(message)

    @staticmethod
    def send_message_to_telegram(message):
        chat_id = settings.ALERT_CHAT_ID
        bot.send_message(chat_id, message)
