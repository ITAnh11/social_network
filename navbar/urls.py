from django.contrib import admin
from django.urls import path

from .views import SearchListView, navbarView

app_name = 'navbar'
urlpatterns = [
    path('', navbarView.as_view(), name='navbar'),
    path('searchlist/', SearchListView.as_view(), name='searchlist'),    #gửi kí tự name ='' # trả về Response: 'profile' or không tìm thấy
]
#searchlist/ : gửi lên sever 
#get_searchlist/ : sever phản hồi lại kết quả tìm kiếm