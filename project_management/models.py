from django.db import models
from home.models import Department
from django.contrib.auth.models import User
import datetime
from colorfield.fields import ColorField


update_type = [
    ('this_week', 'this_week'),
    ('next_week', 'next_week'),
    ('comment', 'comment'),
    ('summary', 'summary')
]


class Team(models.Model):
    name = models.CharField(max_length=1000, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User)
    color = ColorField(default='#FF0000', format="hexa")

    def __str__(self):
        return f'{self.name} Team'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=None)

    def __str__(self):
        return f"{self.user.username}'s Leave"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Status(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Vendor(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class VendorSupervisor(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=200, default='', null=True)
    profile_picture = models.FileField(upload_to='images/')

    def __str__(self):
        return f'{self.name} ({self.vendor})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProjectInfo(models.Model):
    name = models.CharField(max_length=255, default='', unique=True)
    project_id = models.CharField(max_length=255, unique=True, default='', null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_by')
    description = models.TextField(max_length=1000, default='', null=True)
    members = models.ManyToManyField(User)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    vendor_supervisors = models.ManyToManyField(VendorSupervisor)
    ulka_supervisors = models.ManyToManyField(User)
    departments = models.ManyToManyField(Department)
    teams = models.ManyToManyField(Team)
    tags = models.ManyToManyField(Tag)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=None, null=True)
    deadline = models.DateField(default=None, null=True)
    entry_date = models.DateField(default=datetime.date.today, null=True)
    last_updated = models.DateTimeField(default=datetime.datetime.now, null=True)
    ulka_manager = models.ManyToManyField(User)
    ulka_pm = models.ManyToManyField(User)
    progress = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class WeeklyUpdate(models.Model):
    week = models.IntegerField()
    created_at = models.DateTimeField(default=None, null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creator_pp_url = models.CharField(max_length=200, default='', null=True)
    # type = models.CharField(max_length=100, choices=update_type, default='this_week')
    description_this_week = models.TextField(max_length=1000, default='', null=True)
    description_next_week = models.TextField(max_length=1000, default='', null=True)
    description_comment = models.TextField(max_length=1000, default='', null=True)
    description_summary = models.TextField(max_length=1000, default='', null=True)

    def __str__(self):
        return f'week-{self.week} project-{self.project.name} user-{self.creator.profileinfo.office_id_no}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
