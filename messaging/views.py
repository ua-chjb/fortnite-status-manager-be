from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Conversation, Message, GameInvite
from .serializers import ConversationSerializer, MessageSerializer, GameInviteSerializer

# conversations (buckets)
@api_view(["GET", "POST"])
def conversation_list(request):
    if request.method == "GET":
        conversations = Conversation.objects.filter(
            participants=request.user # change to request.user when testing completed
        ).prefetch_related("participants").order_by("-updated_at")
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
    
@api_view(["GET"])
def conversation_detail(request, pk):
    conversation = Conversation.objects.prefetch_related("participants").get(pk=pk)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data)

# messages (detail)
@api_view(["GET", "POST"])
def message_list(request, conversation_pk):

    conversation = Conversation.objects.get(pk=conversation_pk)

    if request.method=="GET":
        messages = conversation.messages.select_related("sender")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation) # sender = request.user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# game invites
@api_view(["GET", "POST"])
def invite_list(request, conversation_pk):

    conversation = Conversation.objects.get(pk=conversation_pk)

    if request.method == "GET":
        invites = conversation.invites.select_related("sender")
        serializer = GameInviteSerializer(invites, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = GameInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite = serializer.save(sender=request.user, conversation=conversation) # sender = request.user
        return Response(GameInviteSerializer(invite).data, status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def invite_accept(request, pk):
    invite = GameInvite.objects.select_related("sender").get(pk=pk)
    invite.status = GameInvite.Status.ACCEPTED
    invite.responded_at = timezone.now()
    invite.save()
    return Response(GameInviteSerializer(invite).data)

@api_view(["POST"])
def invite_decline(request, pk):
    invite = GameInvite.objects.select_related("sender").get(pk=pk)
    invite.status = GameInvite.Status.DECLINED
    invite.responded_at = timezone.now()
    invite.save()
    return Response(GameInviteSerializer(invite).data)
