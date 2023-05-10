from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

from friend.models import User, FriendRequest
from friend.serializers import UserSerializer, AcceptedFriendRequestSerializer, AllFriendRequestSerializer, IncomingFriendRequestSerializer, SendFriendRequestSerializer, FriendsSerializer, DeleteFriendRequestSerializer, RejectedFriendRequestSerializer
from django.urls import path


class PeopleViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/send_friend_requests/', self.send_friend_requests, name='send_friend_requests'),
        ]
        return custom_urls + urls

    def send_friend_requests(self, request, user_id):
        # Получаем текущего пользователя
        from_user = request.user

        # Получаем пользователя, которому хотим отправить запрос
        if User.objects.filter(id=user_id).first() is None:
            return Response({'status': 'Не существует пользователя к которому отправляем заявку в друзья'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = User.objects.get(id=user_id)

        if from_user == to_user:
            return Response({'status': 'Ошибка, нельзя отправит запрос в друзья себе'}, status=status.HTTP_400_BAD_REQUEST)

        # Если заявка уже есть, то нельзя отправить её ещё раз
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first() is not None:
            return Response({'status': 'Ошибка, нельзя отправить несколько запросов одному и тому же человеку'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запрос на дружбу
        friend_request = FriendRequest(from_user=from_user, to_user=to_user)

        # Сохраняем запрос на дружбу
        friend_request.save()

        # Возвращаем успешный ответ
        return Response({'status': 'Запрос отправлен'}, status=status.HTTP_201_CREATED)


class FriendRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = FriendRequest.objects.all()
    serializer_class = AllFriendRequestSerializer
    permission_classes = (IsAuthenticated, )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/check_status', self.check_status, name='check_status'),
            path('<int:user_id>/accept', self.accept, name='accept'),
            path('<int:user_id>/reject', self.reject, name='reject'),
        ]
        return custom_urls + urls

    def accept(self, request, user_id):
        # Получаем пользователя, запрос которого хотим принять
        if User.objects.filter(id=user_id).first() is None:
            return Response({'status': 'Не существует пользователя, которого хотим проверить'}, status=status.HTTP_400_BAD_REQUEST)

        now_user = request.user

        # Входящее
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user,
            to_user=user_id,
            status__in=['incoming', 'rejected']
        ).first()
        # Исходящее
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=now_user,
            status__in=['sent', 'rejected']
        ).first()

        if friends_request_to is None:
            return Response({'status': f'Нет заявки `incoming` или `rejected` от {now_user} к {user_id}'}, status=status.HTTP_400_BAD_REQUEST)

        if friends_request_from is None:
            return Response({'status': f'Нет заявки `sent` или `rejected` от {user_id} к {now_user}'}, status=status.HTTP_400_BAD_REQUEST)

        friends_request_to.status = 'friend'
        friends_request_from.status = 'friend'

        friends_request_to.save()
        friends_request_from.save()

        serializer = AcceptedFriendRequestSerializer(friends_request_to, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def reject(self, request, user_id):
        # Получаем пользователя, запрос которого хотим принять
        if User.objects.filter(id=user_id).first() is None:
            return Response({'status': 'Не существует пользователя, которого хотим проверить'}, status=status.HTTP_400_BAD_REQUEST)

        now_user = request.user

        # Входящее
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user,
            to_user=user_id,
            status='incoming',
        ).first()
        # Исходящее
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=now_user,
            status='sent',
        ).first()

        if friends_request_to is None:
            return Response({'status': f'Нет заявки `incoming` от {now_user} к {user_id}'}, status=status.HTTP_400_BAD_REQUEST)

        if friends_request_from is None:
            return Response({'status': f'Нет заявки `sent` от {user_id} к {now_user}'}, status=status.HTTP_400_BAD_REQUEST)

        friends_request_to.status = 'rejected'
        friends_request_from.status = 'rejected'

        friends_request_to.save()
        friends_request_from.save()

        serializer = RejectedFriendRequestSerializer(friends_request_to, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def check_status(self, request, user_id):
        # Получаем текущего пользователя
        from_user = request.user

        # Получаем пользователя, статус с которым хотим проверить
        if User.objects.filter(id=user_id).first() is None:
            return Response({'status': 'Не существует пользователя, которого хотим проверить'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = User.objects.get(id=user_id)

        if from_user == to_user:
            return Response({'status': 'Ошибка, нельзя проверить свой же статус'}, status=status.HTTP_400_BAD_REQUEST)

        friend_status = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
        if friend_status is None:
            return Response({'status': 'Запрос в друзья ещё не был отправлен'}, status=status.HTTP_200_OK)
        else:
            serializer = AllFriendRequestSerializer(friend_status, many=False)
            return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='incoming_requests')
    def incoming_requests(self, request):
        # Получаем все входящие запросы
        incoming_requests = FriendRequest.objects.filter(to_user=request.user, status='sent')

        # Сериализуем запросы в друзья
        serializer = IncomingFriendRequestSerializer(incoming_requests, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='submitted_requests')
    def submitted_requests(self, request):
        # Получаем все исходящие заявки
        incoming_requests = FriendRequest.objects.filter(from_user=request.user, status='sent')

        # Сериализуем запросы в друзья
        serializer = SendFriendRequestSerializer(incoming_requests, many=True)

        return Response(serializer.data)


class FriendsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = FriendRequest.objects.all()
    serializer_class = AllFriendRequestSerializer
    permission_classes = (IsAuthenticated, )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.friends, name='friends'),
            path('<int:user_id>/delete', self.delete, name='friends_delete'),
        ]
        return custom_urls + urls

    def friends(self, request):
        friends = FriendRequest.objects.filter(
            from_user=request.user,
            status='friend'
        )
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)

    def delete(self, request, user_id):
        friends_request_to = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user_id,
            status='friend'
        ).first()
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=request.user,
            status='friend'
        ).first()

        # Получаем пользователя, которого хотим удалить из друзей
        if User.objects.filter(id=user_id).first() is None:
            return Response({'status': 'Не существует пользователя, которого хотим проверить'}, status=status.HTTP_400_BAD_REQUEST)

        # Если они не друзья
        if friends_request_to is None:
            return Response({'status': 'С данным пользователем вы не друзья'}, status=status.HTTP_400_BAD_REQUEST)

        friends_request_to.status = 'rejected'
        friends_request_from.status = 'rejected'

        friends_request_to.save()
        friends_request_from.save()

        serializer = DeleteFriendRequestSerializer(friends_request_to, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
