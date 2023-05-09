from django.contrib import admin
from friend.models import User, Friendship, ApplicationToFriends

# Register your models here.
admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(ApplicationToFriends)