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

from friend.views import FriendRequestViewSet, PeopleViewSet, FriendsViewSet


people_router = routers.SimpleRouter()
people_router.register(r'people', PeopleViewSet)

friend_request_router = routers.SimpleRouter()
friend_request_router.register(r'friend_request', FriendRequestViewSet, basename='friend_request')


urlpatterns = [
    path("admin/", admin.site.urls),

    # Авторизация по токенам
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'api/v1/auth/', include('djoser.urls.authtoken')),

    # Авторизация по сессии
    path('api/v1/session_auth/', include('rest_framework.urls')),


    # Вывод всех пользователей | конкретного пользователя
    path('api/v1/', include(people_router.urls)),

    # Отправка заявки в друзья
    path('api/v1/people/<int:user_id>/send_friend_requests/', PeopleViewSet.as_view({'post': 'send_friend_requests'}), name='send_friend_request'),

    # Вывод всех заявок в друзья
    path('api/v1/', include(friend_request_router.urls)),

    # Проверка статуса дружбы
    path('api/v1/friend_request/<int:user_id>/check_status/', FriendRequestViewSet.as_view({'get': 'check_status'}), name='check_status'),
    path('api/v1/friend_request/<int:user_id>/accept/', FriendRequestViewSet.as_view({'post': 'accept'}), name='accept_request'),
    path('api/v1/friend_request/<int:user_id>/reject/', FriendRequestViewSet.as_view({'post': 'reject'}), name='reject_request'),

    # Вывод списка друзей
    path('api/v1/friends/', FriendsViewSet.as_view({'get': 'friends'}), name='friends'),
    path('api/v1/friends/<int:user_id>/delete/', FriendsViewSet.as_view({'delete': 'delete'}), name='friend_delete'),
]
