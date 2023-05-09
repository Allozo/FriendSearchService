from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Friendship(models.Model):
    user_id_1 = models.ManyToManyField(User, related_name='+')
    user_id_2 = models.ManyToManyField(User, related_name='+')


class ApplicationToFriends(models.Model):
    user_id_1 = models.ManyToManyField(User, related_name='+')
    user_id_2 = models.ManyToManyField(User, related_name='+')
