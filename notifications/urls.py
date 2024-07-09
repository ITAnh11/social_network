from django.urls import path
from .views import GetNotifications

app_name = 'notifications'
urlpatterns = [
    path('get_notifications/', GetNotifications.as_view(), name='get_notifications'),
]