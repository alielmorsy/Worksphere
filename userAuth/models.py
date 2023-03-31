from django.db.models import CASCADE


from django.contrib.auth.models import AbstractUser
from djongo.models import ArrayReferenceField, ObjectIdField


class User(AbstractUser):
    _id = ObjectIdField()
    userFriends = ArrayReferenceField(to="self", related_name="friends", on_delete=CASCADE)

    def __str__(self):
        return f"ID: {self._id}, userName: {self.username}"
