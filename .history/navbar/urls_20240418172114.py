from django.contrib import admin
from django.urls import path
from . import views

app_name = 'navbar'
urlpatterns = [
    path('', views.navbar, name='navbar'),
    path('searchlist/', searchList.asView(), name='searchlist'),
    path('get_searchlist/', getSearchList.asView(), name='get_searchList')
]
#searchlist/ : gửi lên sever 
#get_searchlist/ : sever phản hồi lại kết quả tìm kiếm