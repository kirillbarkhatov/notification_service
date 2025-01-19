from datetime import datetime
from django.core.mail import send_mail
from django.utils.timezone import now

import requests

from config.settings import BOT_TOKEN, DEFAULT_FROM_EMAIL
from .models import NotifyAttempt, Notify


def send_telegram_notify(chat_id, notify_instance):
    """Сервис для отправки уведомлений в телеграм"""

    message = notify_instance.message

    params = {
        "text": message,
        "chat_id": chat_id,
    }

    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params)
        response_data = response.json()  # Telegram API возвращает JSON-ответ

        # Проверка успешности ответа
        if response.status_code == 200 and response_data.get("ok"):
            # Сохранение успешной попытки
            NotifyAttempt.objects.create(
                attempted_at=datetime.now(),
                status=NotifyAttempt.SUCCESS,
                service=NotifyAttempt.TELEGRAM,
                server_response=response.text,
                notify=notify_instance,
            )
            return {
                "status": "success",
                "message_id": response_data["result"]["message_id"],
                "chat_id": response_data["result"]["chat"]["id"],
                "timestamp": response_data["result"]["date"],
            }
        else:
            # Сохранение неуспешной попытки
            NotifyAttempt.objects.create(
                attempted_at=datetime.now(),
                status=NotifyAttempt.FAILURE,
                service=NotifyAttempt.TELEGRAM,
                server_response=response.text,
                notify=notify_instance,
            )
            return {
                "status": "error",
                "error_code": response_data.get("error_code", "unknown"),
                "description": response_data.get("description", "No description provided"),
            }
    except Exception as e:
        # Сохранение попытки при исключении
        NotifyAttempt.objects.create(
            attempted_at=datetime.now(),
            status=NotifyAttempt.FAILURE,
            service=NotifyAttempt.TELEGRAM,
            server_response=str(e),
            notify=notify_instance,
        )
        return {
            "status": "error",
            "error": str(e),
        }


def send_email_notify(recipient, notify_instance, subject="Уведомление"):
    """
    Сервис для отправки уведомлений по почте и сохранения статуса попытки.

    :param recipient: Email-адрес получателя
    :param notify_instance: Экземпляр модели Notify
    :param subject: Тема письма
    """
    # Берем сообщение из notify_instance
    message = notify_instance.message

    try:
        # Отправляем письмо
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [recipient])
        response = f"{recipient}: Успешно отправлено"

        # Сохраняем успешную попытку
        NotifyAttempt.objects.create(
            attempted_at=now(),
            status=NotifyAttempt.SUCCESS,
            service=NotifyAttempt.MAIL,
            server_response=response,
            notify=notify_instance,
        )
        return {
            "status": "success",
            "recipient": recipient,
            "response": response,
        }
    except Exception as e:
        # Сохраняем неуспешную попытку
        response = f"{recipient}: Ошибка: {str(e)}"
        NotifyAttempt.objects.create(
            attempted_at=now(),
            status=NotifyAttempt.FAILURE,
            service=NotifyAttempt.MAIL,
            server_response=response,
            notify=notify_instance,
        )
        return {
            "status": "error",
            "recipient": recipient,
            "error": str(e),
        }
