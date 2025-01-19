from rest_framework import generics

from .models import Notify
from .serializers import NotifySerializer


class NotifyCreateApiView(generics.CreateAPIView):
    """Создание уведомления"""

    serializer_class = NotifySerializer

