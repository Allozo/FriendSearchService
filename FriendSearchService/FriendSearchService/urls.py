"""
URL configuration for FriendSearchService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers

from friend.views import UserViewSet, FriendRequestListView, send_friend_request


user_router = routers.SimpleRouter()
user_router.register(r'user', UserViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Вывод всех пользователей
    path('api/v1/', include(user_router.urls)),

    # Авторизация по токенам
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'api/v1/auth/', include('djoser.urls.authtoken')),

    # Авторизация по сессии
    path('api/v1/session_auth/', include('rest_framework.urls')),

    # Вывод всех заявок в друзья
    path('api/v1/request_friends/', FriendRequestListView.as_view()),

    # Отправка заявки в друзья
    path('api/v1/send_friend_request/<int:user_id>', send_friend_request),

    # path('api/v1/users/', UsersAPIList.as_view()),
    # path('api/v1/user/<int:pk>', UserAPIView.as_view()),
]
