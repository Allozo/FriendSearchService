from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from friend.models import User, FriendRequest
from friend.serializers import UserSerializer, FriendRequestSerializer
from django.urls import path

class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )


class FriendRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = (IsAuthenticated, )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/send/', self.send, name='send'),
        ]
        return custom_urls + urls

    def send(self, request, user_id):
        # Получаем текущего пользователя
        from_user = request.user

        # Получаем пользователя, которому хотим отправить запрос
        if not User.objects.filter(id=user_id).first():
            return Response({'status': 'Не существует пользователя к которому отправляем заявку в друзья'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = User.objects.get(id=user_id)

        if from_user == to_user:
            return Response({'status': 'Ошибка, нельзя отправит запрос в друзья себе'}, status=status.HTTP_400_BAD_REQUEST)

        # Если заявка уже есть, то нельзя отправить её ещё раз
        if FriendRequest.objects.get(from_user=from_user, to_user=to_user):
            return Response({'status': 'Ошибка, нельзя отправить несколько запросов одному и тому же человеку'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запрос на дружбу
        friend_request = FriendRequest(from_user=from_user, to_user=to_user)

        # Сохраняем запрос на дружбу
        friend_request.save()

        # Возвращаем успешный ответ
        return Response({'status': 'Запрос отправлен'}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='incoming_requests')
    def incoming_requests(self, request):
        # Получаем все входящие запросы в друзья для пользователя, к которому мы обращаемся
        incoming_requests = FriendRequest.objects.filter(to_user=request.user, status='sent')

        # Сериализуем запросы в друзья
        serializer = FriendRequestSerializer(incoming_requests, many=True)

        return Response(serializer.data)
