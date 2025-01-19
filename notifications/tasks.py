import re
from celery import shared_task
from .models import Notify
from .services import send_telegram_notify, send_email_notify  # Предполагается, что эти функции уже реализованы

# Регулярное выражение для проверки email
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


def is_email(recipient):
    """Проверяет, является ли получатель email-адресом."""
    return re.match(EMAIL_REGEX, recipient) is not None


@shared_task
def process_notification(notify_id):
    """
    Задача для отправки уведомлений на основе экземпляра Notify.

    :param notify_id: ID экземпляра Notify
    """
    notify_instance = Notify.objects.get(id=notify_id)
    recipients = notify_instance.recipient if isinstance(notify_instance.recipient, list) else [
        notify_instance.recipient]

    for recipient in recipients:
        if recipient.isdigit():  # Если получатель состоит только из цифр, отправляем в Telegram
            send_telegram_notify_celery.delay(chat_id=recipient, notify_id=notify_id)
        elif is_email(recipient):  # Если это email
            send_email_notify_celery.delay(email=recipient, notify_id=notify_id)


@shared_task
def send_telegram_notify_celery(chat_id, notify_id):
    """
    Задача для отправки уведомлений через Telegram.

    :param chat_id: ID чата Telegram
    :param notify_id: ID экземпляра Notify
    """
    notify_instance = Notify.objects.get(id=notify_id)
    send_telegram_notify(chat_id=chat_id, notify_instance=notify_instance)


@shared_task
def send_email_notify_celery(email, notify_id):
    """
    Задача для отправки уведомлений через Email.

    :param email: Email-адрес получателя
    :param notify_id: ID экземпляра Notify
    """
    notify_instance = Notify.objects.get(id=notify_id)
    send_email_notify(recipient=email, notify_instance=notify_instance)
