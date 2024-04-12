from django.urls import path

from . import views

app_name = 'navbar'
urlpatterns = [
    path('', views.index, name='navbar'),
]