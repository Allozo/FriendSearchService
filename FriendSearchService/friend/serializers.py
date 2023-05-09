from rest_framework import fields, serializers

from friend.models import User, Friendship, ApplicationToFriends


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('user_1', 'user_2')


class ApplicationToFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationToFriends
        fields = ('user_1', 'user_2')