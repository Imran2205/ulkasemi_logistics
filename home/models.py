import datetime

from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from phonenumber_field.modelfields import PhoneNumberField


stat2 = [
    ('general', 'general'),
    ('admin', 'admin')
]

designations = [
    ('Sr. TM', 'Sr. TM'),
    ('TM', 'TM'),
    ('ATM', 'ATM'),
    ('Sr. Engineer', 'Sr. Engineer'),
    ('Engineer', 'Engineer'),
    ('Assistant Engineer', 'Assistant Engineer'),
    ('Trainee Engineer', 'Trainee Engineer'),
    ('N/A', 'N/A')
]


class Department(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return f'{self.name} Department'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_id_no = models.CharField(max_length=100, unique=True)
    profile_type = models.CharField(max_length=100, choices=stat2, default='general')
    notification_token = models.CharField(max_length=200, default='', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    profile_picture_url = models.CharField(max_length=200, default='', null=True)
    designation = models.CharField(max_length=100, choices=designations, default='N/A')
    role = models.ManyToManyField(Role)
    gf_email = models.CharField(max_length=100, default='na')
    contact_no = PhoneNumberField(blank=True)
    blood_group = models.CharField(max_length=6, default='n/a')
    last_activity = models.DateTimeField(default=datetime.datetime.now, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # if not self.profile_picture_url:
        #     self.profile_picture_url = SocialAccount.objects.get(user=self.user).extra_data['picture']
        # super(ProfileInfo, self).save(*args, **kwargs)
        super(ProfileInfo, self).save(*args, **kwargs)
