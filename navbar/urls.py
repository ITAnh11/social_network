from django.contrib import admin
from django.urls import path
from . import views

app_name = 'navbar'
urlpatterns = [
    path('', views.navbar, name='navbar'),
]