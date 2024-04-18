from django.contrib import admin
from django.urls import path
from . import views

from .views import searchList, getSearchList

app_name = 'navbar'
urlpatterns = [
    path('', views.navbar, name='navbar'),
    path('searchlist/', searchList.asView(), name='searchlist'),    #gửi kí tự name =''
    path('get_searchlist/', getSearchList.asView(), name='get_searchList')# trả về Respone: 'profile' or không tìm thấy
]
#searchlist/ : gửi lên sever 
#get_searchlist/ : sever phản hồi lại kết quả tìm kiếm