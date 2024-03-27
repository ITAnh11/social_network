from django.urls import path 
from . import views 

app_name = 'post_app'

urlpatterns = [ 
    path('', views.index, name = 'index'), 
    path('home/', views.home, name = 'home'),
    path('<name>/<id>', views.pathview, name='pathview'), 
    path('getuser/', views.qryview, name='qryview'),
    path("showform/", views.showform, name="showform"), 
    path("getform/", views.getform, name='getform'),
] 