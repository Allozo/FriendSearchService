from rest_framework import fields, serializers

from friend.models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class FriendRequestSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'created_at', 'status')
        read_only_fields = ('id', 'created_at', 'status')

    def get_status(self, obj):  
        return obj.get_status_display()