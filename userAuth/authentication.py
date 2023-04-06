from bson import ObjectId
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils.translation import gettext_lazy as _

from userAuth.auth import User


class UserAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token["user_id"]
            return User.objects.get(pk=ObjectId(user_id))
        except:
            raise InvalidToken(_("Invalid Login Token"))
