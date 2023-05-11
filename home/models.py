from django.db import models
from django.contrib.auth.models import User


stat2 = [
    ('general', 'general'),
    ('admin', 'admin')
]


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id_no = models.CharField(max_length=100, unique=True)
    profile_type = models.CharField(max_length=100, choices=stat2, default='general')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
