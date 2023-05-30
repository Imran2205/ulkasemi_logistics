import datetime

from django.db import models
from django.contrib.auth.models import User


booked_opt = [
    ('yes', 'yes'),
    ('no', 'no'),
]

stat2 = [
    ('general', 'general'),
    ('admin', 'admin')
]


class BookingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    booked = models.CharField(max_length=100, choices=booked_opt, default='no')
    email = models.CharField(null=True, max_length=100)
    office_id = models.CharField(null=True, max_length=10)
    name = models.CharField(null=True, max_length=50)

    def __str__(self):
        return f'{self.user.profileinfo.office_id_no} {self.date}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProfileInfoLunch(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=100, choices=stat2, default='general')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(ProfileInfoLunch, self).save(*args, **kwargs)
