from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render

from friend.models import User, Friendship, ApplicationToFriends
from friend.serializers import UserSerializer


class UserViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UsersAPIList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserAPIView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
