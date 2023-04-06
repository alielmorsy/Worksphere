from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser
from djongo.models import ArrayReferenceField, ObjectIdField
from django.utils.translation import gettext_lazy as _

# Company.objects.filter(users__user__username="alielmorsy")[0]

class User(AbstractUser):
    _id = ObjectIdField()
    first_name = models.CharField(_("firstName"), max_length=150, blank=True)
    last_name = models.CharField(_("lastName"), max_length=150, blank=True)
    email = models.EmailField(_("emailAddress"), blank=True)
    userFriends = ArrayReferenceField(to="self", related_name="friends", on_delete=CASCADE)

    def __str__(self):
        return f"ID: {self._id}, userName: {self.username}"

    def id(self):
        return self._id