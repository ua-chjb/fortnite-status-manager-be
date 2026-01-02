from rest_framework import serializers
from .models import Conversation, Message, GameInvite
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "created_at"]
        read_only_fields = ["id", "sender", "created_at"]

class GameInviteSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = GameInvite
        fields = ["id", "sender", "content", "status", "created_at", "responded_at"]
        read_only_fields = ["id", "sender", "created_at", "responded_at"]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "name", "is_group", "participants", "updated_at"]
        read_only_fields = ["id", "updated_at"]