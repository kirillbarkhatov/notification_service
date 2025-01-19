from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta
from .serializers import NotifySerializer
from .tasks import process_notification


class NotifyCreateApiView(generics.CreateAPIView):
    """Создание уведомления"""

    serializer_class = NotifySerializer

    def perform_create(self, serializer):
        """
        Переопределяем метод для выполнения действий после создания объекта Notify.
        """
        # Сохраняем объект Notify
        notify_instance = serializer.save()

        # Рассчитываем время выполнения задачи
        delay = notify_instance.delay
        if delay == 0:
            eta = now()
        elif delay == 1:
            eta = now() + timedelta(hours=1)
        elif delay == 2:
            eta = now() + timedelta(days=1)
        else:
            raise ValueError("Величина задержки отправки указана некорректно")

        # Планируем задачу Celery
        process_notification.apply_async(args=[notify_instance.id], eta=eta)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод create для возврата кастомного ответа.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Уведомление создано и отправлено на обработку."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )