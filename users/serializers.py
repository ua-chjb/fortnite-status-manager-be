from rest_framework import serializers
from .models import User, Friendship
from status.serializers import UserStatusSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "epic_display_name"]
        read_only_fields = fields

class FriendshipSerializer(serializers.ModelSerializer):

    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "friend"]

class HomeFeedFriendSerializer(serializers.ModelSerializer):
    status=UserStatusSerializer(read_only=True)

    class Meta:
        model=User
        fields = ["id", "epic_display_name", "status"]

class HomeFeedSerializer(serializers.ModelSerializer):
    friend = HomeFeedFriendSerializer(read_only=True)
    class Meta:
        model = Friendship
        fields = ["id", "friend"]