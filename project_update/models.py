from django.db import models
from home.models import Department
from django.contrib.auth.models import User


update_type = [
    ('this_week', 'this_week'),
    ('next_week', 'next_week'),
    ('comment', 'comment'),
    ('summary', 'summary')
]


class Team(models.Model):
    name = models.CharField(max_length=1000, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department', null=True)
    members = models.ManyToManyField(User, null=True, related_name='members')

    def __str__(self):
        return f'{self.name} Team'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class UlkaSupervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, null=True, related_name='team_members')
    teams = models.ManyToManyField(Team, null=True, related_name='teams')

    def __str__(self):
        return f'{self.user.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Status(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Vendor(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class VendorSupervisor(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor', null=True)
    email = models.CharField(max_length=200, default='', null=True)
    profile_picture = models.FileField(upload_to='images/')

    def __str__(self):
        return f'{self.name} ({self.vendor})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProjectInfo(models.Model):
    name = models.CharField(max_length=1000, default='', unique=True)
    id = models.CharField(max_length=100, unique=True, default='', null=True)
    description = models.TextField(max_length=1000, default='', null=True)
    members = models.ManyToManyField(User, null=True, related_name='members')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor', null=True)
    vendor_supervisors = models.ManyToManyField(VendorSupervisor, null=True, related_name='vendor_supervisors')
    ulka_supervisors = models.ManyToManyField(UlkaSupervisor, null=True, related_name='ulka_supervisors')
    departments = models.ManyToManyField(Department, null=True, related_name='departments')
    teams = models.ManyToManyField(Team, null=True, related_name='teams')
    tags = models.ManyToManyField(Tag, null=True, related_name='tags')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status', null=True)
    start_date = models.DateTimeField(default=None, null=True)
    deadline = models.DateTimeField(default=None, null=True)
    entry_date = models.DateTimeField(default=None, null=True)
    last_updated = models.DateTimeField(default=None, null=True)
    progress = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class WeeklyUpdate(models.Model):
    week = models.IntegerField()
    created_at = models.DateTimeField(default=None, null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, related_name='project', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', null=True)
    type = models.CharField(max_length=100, choices=update_type, default='this_week')
    description = models.TextField(max_length=1000, default='', null=True)

    def __str__(self):
        return f'week-{self.week} project-{self.project.name} user-{self.creator.profileinfo.office_id_no}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
