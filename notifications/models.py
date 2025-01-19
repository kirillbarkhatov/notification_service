from django.db import models


class Notify(models.Model):
    """Модель уведомления"""

    DELAY_CHOICES = [
        (0, 'Отправить без задержки'),
        (1, 'Отправить с задержной 1 час'),
        (2, 'Отправить с задержной 2 часа'),
    ]

    message = models.CharField(max_length=1024, verbose_name="Сообщение")
    recipient = models.JSONField(verbose_name="Получатели")
    delay = models.IntegerField(choices=DELAY_CHOICES, verbose_name="Задержка отправки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.message[:15]

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = [
            "id",
        ]


class NotifyAttempt(models.Model):
    """Модель попытки отправки уведомления"""

    # статусы попытки отправки
    SUCCESS = "success"
    FAILURE = "failure"

    STATUS_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAILURE, "Не успешно"),
    ]

    # используемый сервис для отправки
    MAIL = "mail"
    TELEGRAM = "telegram"

    SERVICE_CHOICES = [
        (MAIL, "Почта"),
        (TELEGRAM, "Телеграм"),
    ]

    attempted_at = models.DateTimeField(
        verbose_name="Дата и время попытки отправки",
    )

    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )

    service = models.CharField(
        max_length=8,
        choices=SERVICE_CHOICES,
        verbose_name="Сервис",
    )

    server_response = models.TextField(
        null=True,
        blank=True,
        verbose_name="Ответ сервера",
    )

    notify = models.ForeignKey(
        Notify,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Уведомление",
    )

    def __str__(self):
        return f"{self.pk} - {self.attempted_at}"

    class Meta:
        verbose_name = "Попытка уведомления"
        verbose_name_plural = "Попытки уведомления"
        ordering = [
            "id",
        ]
