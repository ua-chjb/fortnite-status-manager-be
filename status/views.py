from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserStatus
from .serializers import UserStatusSerializer

@api_view(["GET", "PATCH"])
def my_status(request):
    status, _ = UserStatus.objects.get_or_create(user=request.user)

    if request.method=="GET":
        serializer = UserStatusSerializer(status)
        return Response(serializer.data)
    
    elif request.method=="PATCH":
        serializer = UserStatusSerializer(status, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
