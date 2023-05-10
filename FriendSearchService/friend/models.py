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
            ('incoming', 'Есть входящая заявка'),
            ('rejected', 'Заявка отклонена'),
            ('friend', 'Друзья'),
        ),
        default='sent',
        max_length=20
    )

    class Meta:
        unique_together = ('from_user', 'to_user')
