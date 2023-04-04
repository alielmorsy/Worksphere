from django.shortcuts import render
# Create your views her
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CreateChannelSerializer, SendMassageSerializer
from .validators import Validate_channel_and_user


class CreateChannelView(APIView):
    raise_exception = True

    def get(self, request):
        MESSAGES_PER_PAGE = 40
        userid = request.query_params['user']
        channelid = request.query_params['channelid']
        No_messages = int(request.query_params['pages']) * MESSAGES_PER_PAGE
        validated_data = Validate_channel_and_user(userid, channelid)
        channel = validated_data.channel
        messages = []
        for message in channel.messages.all()[:No_messages]:
            messages.append(message.get())

        response = {
            "channelId": channelid,
            "numberOfMessages": No_messages,
            "messages": messages
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = CreateChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.create(serializer.validated_data)
        channel.save()
        response = {
            "channel": str(channel.pk),
            "State": 'channel named ' + channel.channelName + ' Created succefully'
        }
        return Response(response)


class SendMessageView(APIView):
    raise_exception = True

    def post(self, request, *args, **kwargs):
        serializer = SendMassageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.create(serializer.validated_data)
        message.save()
        response = {
            "message": f"To: {message.sender.username} Body: {message.messageBody}",
        }
        return Response(response)
