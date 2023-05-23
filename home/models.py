from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


stat2 = [
    ('general', 'general'),
    ('admin', 'admin')
]


class Department(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)

    def __str__(self):
        return f'{self.name} Department'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_id_no = models.CharField(max_length=100, unique=True)
    profile_type = models.CharField(max_length=100, choices=stat2, default='general')
    notification_token = models.CharField(max_length=200, default='', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    profile_picture_url = models.CharField(max_length=200, default='', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # if not self.profile_picture_url:
        #     self.profile_picture_url = SocialAccount.objects.get(user=self.user).extra_data['picture']
        # super(ProfileInfo, self).save(*args, **kwargs)
        super(ProfileInfo, self).save(*args, **kwargs)
