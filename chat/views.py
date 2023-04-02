from django.shortcuts import render
# Create your views her
from rest_framework import serializers
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializer import ChannelSerializer , MassageSerializer




class channelView(APIView):
    raise_exception = True
    def post(self, request, *args, **kwargs):
        serializer = ChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.create(serializer.validated_data)
        channel.save()
        response = {
            "channel": str(channel._id),
            "State": 'channel named ' + channel.channelName +' Created succefully'
        }
        return Response(response)
    
class messageView(APIView):
    raise_exception = True
    def post(self, request, *args, **kwargs):
        serializer = MassageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.create(serializer.validated_data)
        message.save()
        response = {
            "message": f"To: {message.sender} Body: {message.messageBody}",
        }
        return Response(response)