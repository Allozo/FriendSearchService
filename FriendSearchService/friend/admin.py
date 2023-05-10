from django.contrib import admin
from friend.models import FriendRequest  # pylint: disable=E0401

# Register your models here.
admin.site.register(FriendRequest)
