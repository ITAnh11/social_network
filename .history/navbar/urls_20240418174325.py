from django.contrib import admin
from django.urls import path
from . import views

from .views import searchListView, getSearchListView

app_name = 'navbar'
urlpatterns = [
    path('', views.navbar, name='navbar'),
    path('searchlist/', searchListView.asView(), name='searchlist'),    #gửi kí tự name =''
    path('get_searchlist/', getSearchListView.asView(), name='get_searchList')# trả về Response: 'profile' or không tìm thấy
]
#searchlist/ : gửi lên sever 
#get_searchlist/ : sever phản hồi lại kết quả tìm kiếm