from rest_framework import fields, serializers

from friend.models import User, FriendRequest


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

    def get_status(self, obj):
        return obj.get_status_display()


class AcceptedFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')

    class Meta:
        model = FriendRequest
        fields = ('user', )


class RejectedFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='to_user.id')

    class Meta:
        model = FriendRequest
        fields = ('user', )


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('from_user', 'created_at')

    def get_status(self, obj):
        return obj.get_status_display()


class SendFriendRequestSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('to_user', 'created_at', 'status')
        read_only_fields = ('id', 'created_at', 'status')

    def get_status(self, obj):
        return obj.get_status_display()


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('to_user', 'created_at')


class DeleteFriendRequestSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('to_user', 'created_at', 'status')
        read_only_fields = ('id', 'created_at', 'status')

    def get_status(self, obj):
        return obj.get_status_display()