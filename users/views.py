from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from .serializers import UserSerializer, FriendshipSerializer, HomeFeedSerializer

@api_view(["GET"])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(["GET"])
def friend_list(request):
    friendships = Friendship.objects.filter(user=request.user).select_related("friend")
    serializer = FriendshipSerializer(friendships, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def home_feed(request):
    friendships = Friendship.objects.filter(
        user=request.user
    ).select_related("friend", "friend__status")
    serializer = HomeFeedSerializer(friendships, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def friend_detail(request, pk):
    friendship = Friendship.objects.select_related(
        "friend", "friend__status"
    ).get(user=request.user, friend_id=pk)
    serializer = HomeFeedSerializer(friendship)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_account(request):
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
