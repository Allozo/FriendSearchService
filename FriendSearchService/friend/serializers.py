from friend.models import FriendRequest, User  # pylint: disable=E0401
from rest_framework import serializers
from rest_framework.fields import Field


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class AllFriendRequestSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'created_at', 'status')
        read_only_fields = ('id', 'created_at', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class AcceptedFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class RejectedFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'created_at', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class SendFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'created_at', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class FriendsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'created_at', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()


class DeleteFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('user', 'created_at', 'status')

    def get_status(self, obj: Field) -> str:
        return obj.get_status_display()
