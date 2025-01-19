from django.urls import path

from . import views
from .apps import NotificationsConfig

app_name = NotificationsConfig.name


urlpatterns = [
    path("api/notify/", views.NotifyCreateApiView.as_view(), name="notify_create"),
]