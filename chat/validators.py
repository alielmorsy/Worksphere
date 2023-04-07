from rest_framework import serializers
from .models import *
from . import models
from rest_framework import serializers
from userAuth.models import User
from .exceptions import  UserNotExists, ChannelNotExists,UserIsNotInChannel
from bson import ObjectId


class Validate_channel_and_user():
    def __init__(self,userid,channelid):
        self.userid = userid
        self.channelid = channelid
        self.validate()
    def validate_and_get_sender(self, userid):
        try:
            user = User.objects.get(_id=ObjectId(userid))
        except:
            raise UserNotExists()
        return user
    
    def validate_and_get_Channel(self, channelid):
        #user = User.objects.get(username=username)
        try:
            channel = models.Channel.objects.get(_id = ObjectId(channelid))
        except:
            raise ChannelNotExists()
        return channel
    def validate(self):      # it will be adjusted later to check if user in company server users
        self.user = self.validate_and_get_sender(self.userid)
        self.channel = self.validate_and_get_sender(self.channelid)
        if self.userid != str(self.channel.createdBy._id):
            raise UserIsNotInChannel()



