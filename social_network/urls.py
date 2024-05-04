"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 
from django.conf import settings
from django.conf.urls.static import static

# import debug_toolbar

from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('homepage/', include('homepage.urls')),
    path('users/', include('users.urls')),
    path('userprofiles/', include('userprofiles.urls')),
    path('posts/', include('posts.urls')),
    path('friends/', include('friends.urls')),

    path('chat/', include('chat.urls')),
    path('comments/', include('comments.urls')),
    path('navbar/', include('navbar.urls')),
    path('reactions/', include('reactions.urls')),
    path("send_message/", views.SendMessage.as_view()),
    path("search/<username>", views.SearchUser.as_view()),
    
    path('notifications/', include('notifications.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'social_network.views.handler404'
