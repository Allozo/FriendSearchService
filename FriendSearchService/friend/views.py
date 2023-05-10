from django.urls import path
from friend.models import FriendRequest, User  # pylint: disable=E0401
from friend.serializers import (  # pylint: disable=E0401
    AcceptedFriendRequestSerializer,
    AllFriendRequestSerializer,
    DeleteFriendRequestSerializer,
    FriendsSerializer,
    IncomingFriendRequestSerializer,
    RejectedFriendRequestSerializer,
    SendFriendRequestSerializer,
    UserSerializer,
)
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class PeopleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_urls(self) -> list[path]:
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/send_friend_requests/',
                self.send_friend_requests,
                name='send_friend_requests',
            ),
        ]
        return custom_urls + urls

    def send_friend_requests(  # pylint: disable=R0911
        self, request: Request, user_id: int
    ) -> Response:
        # Получаем текущего пользователя
        now_user = request.user

        # Получаем пользователя, которому хотим отправить запрос
        if User.objects.filter(id=user_id).first() is None:
            return Response(
                {
                    'status': 'Не существует пользователя к которому отправляем заявку в друзья'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        to_user = User.objects.get(id=user_id)

        if now_user == to_user:
            return Response(
                {'status': 'Ошибка, нельзя отправит запрос в друзья себе'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Если заявка уже есть, то нельзя отправить её ещё раз
        if (
            FriendRequest.objects.filter(
                from_user=now_user, to_user=to_user, status='sent'
            ).first()
            is not None
        ):
            return Response(
                {
                    'status': 'Ошибка, нельзя отправить несколько запросов одному человеку'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Если другой пользователь отклонил заявку
        if (
            FriendRequest.objects.filter(
                from_user=to_user, to_user=now_user, status='rejected'
            ).first()
            is not None
        ):
            return Response(
                {'status': 'Ошибка, вашу заявку отклонили'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Если мы отклонили отклонил заявку
        if (
            FriendRequest.objects.filter(
                from_user=now_user, to_user=to_user, status='rejected'
            ).first()
            is not None
        ):
            friend_request_incoming = FriendRequest.objects.filter(
                from_user=now_user, to_user=to_user, status='rejected'
            ).first()
            friend_request_sent = FriendRequest.objects.filter(
                from_user=to_user, to_user=now_user, status='sent'
            ).first()

            friend_request_incoming.status = 'friend'
            friend_request_sent.status = 'friend'

            friend_request_sent.save()
            friend_request_incoming.save()

            serializer = AcceptedFriendRequestSerializer(
                friend_request_incoming, many=False
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если есть заявка в друзья от другого пользователя
        if (
            FriendRequest.objects.filter(
                from_user=to_user, to_user=now_user, status='sent'
            ).first()
            is not None
        ):
            friend_request_incoming = FriendRequest.objects.filter(
                from_user=now_user, to_user=to_user, status='incoming'
            ).first()
            friend_request_sent = FriendRequest.objects.filter(
                from_user=to_user, to_user=now_user, status='sent'
            ).first()

            friend_request_incoming.status = 'friend'
            friend_request_sent.status = 'friend'

            friend_request_sent.save()
            friend_request_incoming.save()

            serializer = AcceptedFriendRequestSerializer(
                friend_request_incoming, many=False
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Создаем запрос на дружбу
        friend_request_sent = FriendRequest(
            from_user=now_user, to_user=to_user, status='sent'
        )
        friend_request_incoming = FriendRequest(
            from_user=to_user, to_user=now_user, status='incoming'
        )

        # Сохраняем запрос на дружбу
        friend_request_sent.save()
        friend_request_incoming.save()

        serializer = SendFriendRequestSerializer(friend_request_sent, many=False)

        # Возвращаем успешный ответ
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = FriendRequest.objects.all()
    serializer_class = AllFriendRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_urls(self) -> list[path]:
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/check_status', self.check_status, name='check_status'),
            path('<int:user_id>/accept', self.accept, name='accept'),
            path('<int:user_id>/reject', self.reject, name='reject'),
        ]
        return custom_urls + urls

    def accept(  # pylint: disable=R0911
        self, request: Request, user_id: int
    ) -> Response:  # pylint: disable=R0911
        # Получаем пользователя, запрос которого хотим принять
        if User.objects.filter(id=user_id).first() is None:
            return Response(
                {
                    'status': 'Не существует пользователя, которого хотим принять в друзья'
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        now_user = request.user

        # Делаем проверку на существование хоть каких-то заявок

        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user,
            to_user=user_id,
        ).first()
        # Исходящее
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=now_user,
        ).first()

        if friends_request_to is None:
            return Response(
                {'status': f'Нет заявки `incoming`от {now_user} к {user_id}'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if friends_request_from is None:
            return Response(
                {'status': f'Нет заявки `sent`от {user_id} к {now_user}'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 1 случай, где есть входящая заявка и мы её принимаем
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user, to_user=user_id, status='incoming'
        ).first()
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id, to_user=now_user, status='sent'
        ).first()
        if friends_request_to is not None and friends_request_from is not None:
            friends_request_to.status = 'friend'
            friends_request_from.status = 'friend'

            friends_request_to.save()
            friends_request_from.save()

            serializer = AcceptedFriendRequestSerializer(friends_request_to, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # 2 случай, где есть нам отправили заявку, а мы раньше её отклонили
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user, to_user=user_id, status='rejected'
        ).first()
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id, to_user=now_user, status='sent'
        ).first()
        if friends_request_to is not None and friends_request_from is not None:
            friends_request_to.status = 'friend'
            friends_request_from.status = 'friend'

            friends_request_to.save()
            friends_request_from.save()

            serializer = AcceptedFriendRequestSerializer(friends_request_to, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # 3 случай, где мы отправили заявку, но её отклонили
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user, to_user=user_id, status='sent'
        ).first()
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id, to_user=now_user, status='rejected'
        ).first()
        if friends_request_to is not None and friends_request_from is not None:
            return Response(
                {'status': 'Ошибка: Вы не можете принять заявку, так как вам отказали'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'status': 'Ошибка: При принятии заявки произошла ошибка'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def reject(self, request: Request, user_id: int) -> Response:
        # Получаем пользователя, запрос которого хотим принять
        if User.objects.filter(id=user_id).first() is None:
            return Response(
                {'status': 'Не существует пользователя, которого хотим проверить'},
                status=status.HTTP_404_NOT_FOUND,
            )

        now_user = request.user

        # Входящее
        friends_request_to = FriendRequest.objects.filter(
            from_user=now_user,
            to_user=user_id,
            status='incoming',
        ).first()

        if friends_request_to is None:
            return Response(
                {'status': f'Нет заявки `incoming` от {now_user} к {user_id}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friends_request_to.status = 'rejected'

        friends_request_to.save()

        serializer = RejectedFriendRequestSerializer(friends_request_to, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_status(self, request: Request, user_id: int) -> Response:
        # Получаем текущего пользователя
        from_user = request.user

        # Получаем пользователя, статус с которым хотим проверить
        if User.objects.filter(id=user_id).first() is None:
            return Response(
                {'status': 'Не существует пользователя, которого хотим проверить'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        to_user = User.objects.get(id=user_id)

        if from_user == to_user:
            return Response(
                {'status': 'Ошибка, нельзя проверить свой же статус'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_status = FriendRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).first()
        if friend_status is None:
            return Response(
                {'status': 'Запрос в друзья ещё не был отправлен'},
                status=status.HTTP_200_OK,
            )

        serializer = AllFriendRequestSerializer(friend_status, many=False)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='incoming_requests')
    def incoming_requests(self, request: Request) -> Response:
        # Получаем все входящие запросы
        incoming_requests = FriendRequest.objects.filter(
            from_user=request.user, status='incoming'
        )

        # Сериализуем запросы в друзья
        serializer = IncomingFriendRequestSerializer(incoming_requests, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='submitted_requests')
    def submitted_requests(self, request: Request) -> Response:
        # Получаем все исходящие заявки
        incoming_requests = FriendRequest.objects.filter(
            from_user=request.user, status='sent'
        )

        # Сериализуем запросы в друзья
        serializer = SendFriendRequestSerializer(incoming_requests, many=True)

        return Response(serializer.data)


class FriendsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = AllFriendRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_urls(self) -> list[path]:
        urls = super().get_urls()
        custom_urls = [
            path('', self.friends, name='friends'),
            path('<int:user_id>/delete', self.delete, name='friends_delete'),
        ]
        return custom_urls + urls

    def friends(self, request: Request) -> Response:
        friends = FriendRequest.objects.filter(from_user=request.user, status='friend')
        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)

    def delete(self, request: Request, user_id: int) -> Response:
        friends_request_to = FriendRequest.objects.filter(
            from_user=request.user, to_user=user_id, status='friend'
        ).first()
        friends_request_from = FriendRequest.objects.filter(
            from_user=user_id, to_user=request.user, status='friend'
        ).first()

        # Получаем пользователя, которого хотим удалить из друзей
        if User.objects.filter(id=user_id).first() is None:
            return Response(
                {'status': 'Не существует пользователя, которого хотим проверить'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Если они не друзья
        if friends_request_to is None:
            return Response(
                {'status': 'С данным пользователем вы не друзья'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friends_request_to.status = 'rejected'
        friends_request_from.status = 'sent'

        friends_request_to.save()
        friends_request_from.save()

        serializer = DeleteFriendRequestSerializer(friends_request_to, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
