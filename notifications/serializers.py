from rest_framework import serializers

from .models import Notify


class NotifySerializer(serializers.ModelSerializer):
    """Сериализатор для уведомлений"""

    class Meta:
        model = Notify
        fields = "__all__"
