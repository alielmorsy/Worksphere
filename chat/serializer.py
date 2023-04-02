from rest_framework import serializers
from .models import *
from . import models
from rest_framework import serializers
from userAuth.models import User
from .exceptions import  UserDoesnotExist, ChannelDoesnotExist
from bson import ObjectId
# create a serializer



class ChannelSerializer(serializers.ModelSerializer):
    createdBy = serializers.CharField(max_length=32)
    def create(self, validated_data):
        channel = Channel.objects.create(   createdBy =User.objects.get(username=validated_data['createdBy']) , 
                                            channelName=validated_data['channelName'],
                                            channelType=validated_data['channelType'],
                                        )
        channel.messages.add(channel.welcome_massage())
        return channel

    def validate_createdBy_____test(self, createdBy):
        #user = User.objects.get(username=username)
        try:
            user = User.objects.get(username=createdBy)
        except:
            raise UserDoesnotExist()
        return user

    class Meta:
        model = Channel
        fields = ["channelName", "createdBy", "channelType"]
        read_only_fields = ('_id',)

class MassageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=32)
    Channel = serializers.CharField(max_length=32)

    def create(self, validated_data):
        try:
            if validated_data['repliedFrom'] is None:
                replied_from = None
            else:
                replied_from = Message.objects.get(_id=validated_data['repliedFrom'])
        except:
            replied_from = None


        message = Message.objects.create(   sender =User.objects.get(username=validated_data['sender']) , 
                                            messageBody=validated_data['messageBody'],
                                            repliedFrom = replied_from,
                                        )
        Channel.objects.get(_id = ObjectId(validated_data['Channel'])).messages.add(message)
        return message

    def validate_sender_____test(self, sender):
        #user = User.objects.get(username=username)
        try:
            user = User.objects.get(username=sender)
        except:
            raise UserDoesnotExist()
        return user
    
    def validate_Channel_____test(self, Channel):
        #user = User.objects.get(username=username)
        try:
            channel = models.Channel.objects.get(_id = ObjectId(Channel))
        except:
            raise ChannelDoesnotExist()
        return channel

    class Meta:
        model = Message
        fields = ["messageBody", "sender", "repliedFrom" , 'Channel']
        read_only_fields = ('_id',)