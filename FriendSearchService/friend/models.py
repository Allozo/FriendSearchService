from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=(
            ('sent', 'Заявка отправлена'),
            ('rejected', 'Заявка отклонена'),
            ('accepted', 'Заявка принята')
        ),
        default='sent',
        max_length=20
    )