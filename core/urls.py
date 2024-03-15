from django.urls import path
from .views import LoginView, RegisterView, index, LogoutView

app_name = 'core'
urlpatterns = [
    path('', index.as_view(), name='index'),
    path('index/', index.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]