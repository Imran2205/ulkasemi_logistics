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
    last_used_color = models.IntegerField(default=0)

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
    project_id = models.CharField(max_length=255, unique=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_by')
    description = models.TextField(max_length=1000, default='', null=True)
    members = models.ManyToManyField(User, related_name='members')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    vendor_supervisors = models.ManyToManyField(VendorSupervisor)
    ulka_supervisors = models.ManyToManyField(User)
    departments = models.ManyToManyField(Department)
    teams = models.ManyToManyField(Team)
    tags = models.ManyToManyField(Tag)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=datetime.date.today, null=True)
    deadline = models.DateField(default=datetime.date.today, null=True)
    entry_date = models.DateField(default=datetime.date.today, null=True)
    last_updated = models.DateTimeField(default=datetime.datetime.now, null=True)
    ulka_manager = models.ManyToManyField(User, related_name='ulka_manager')
    ulka_pm = models.ManyToManyField(User, related_name='ulka_pm')
    ulka_ack_person = models.ManyToManyField(User, related_name='ulka_ack_person')
    progress = models.IntegerField()
    search_field = models.TextField(max_length=2000, default='', null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def user_directory_path(instance, filename):
    path_of_file = f'files/task_files/{instance.task.project.name}/{instance.task.name}/' \
                   f'{instance.task.assigned_by.username}_{instance.task.assigned_by.profileinfo.office_id_no}/' \
                   f'{instance.task.id}/{instance.task.assigned_by.username}/' + \
                   f'supp_mat_{instance.task.name}_{instance.task.project.id}_{instance.task.id}.{filename.strip().split(".")[-1]}'
    return path_of_file


class TaskInfo(models.Model):
    name = models.CharField(max_length=255, default='')
    task_id = models.CharField(max_length=255, unique=True, null=True)
    details = models.TextField(max_length=1000, default='')
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    task_created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='task_created_by')
    start_date = models.DateField(default=datetime.date.today, null=True)
    deadline = models.DateField(default=datetime.date.today, null=True)
    entry_date = models.DateField(default=datetime.date.today, null=True)
    last_updated = models.DateTimeField(default=datetime.datetime.now, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='assigned_by')
    assigned_to = models.ManyToManyField(User, related_name='assigned_to')
    percent_of_proj = models.IntegerField()
    progress = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.project.name} {self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class TaskSuppFile(models.Model):
    task = models.OneToOneField(TaskInfo, on_delete=models.CASCADE)
    supplementary_file = models.FileField(upload_to=user_directory_path, null=True, default='')

    def __str__(self):
        return self.task.name + "_supp_file"


class WeeklyUpdate(models.Model):
    week = models.IntegerField()
    created_at = models.DateTimeField(default=None, null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creator_pp_url = models.CharField(max_length=200, default='', null=True)
    creator_ofc_id = models.CharField(max_length=10, default='', null=True)
    # type = models.CharField(max_length=100, choices=update_type, default='this_week')
    description_this_week = models.TextField(max_length=1000, default='', null=True)
    description_next_week = models.TextField(max_length=1000, default='', null=True)
    description_comment = models.TextField(max_length=1000, default='', null=True)
    description_summary = models.TextField(max_length=1000, default='', null=True)

    def __str__(self):
        return f'week-{self.week} project-{self.project.name} user-{self.creator.profileinfo.office_id_no}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class WeeklyUpdateTask(models.Model):
    week = models.IntegerField()
    created_at = models.DateTimeField(default=None, null=True)
    task = models.ForeignKey(TaskInfo, on_delete=models.CASCADE, null=True)
    task_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    creator_pp_url = models.CharField(max_length=200, default='', null=True)
    creator_ofc_id = models.CharField(max_length=10, default='', null=True)
    # type = models.CharField(max_length=100, choices=update_type, default='this_week')
    description_this_week = models.TextField(max_length=1000, default='', null=True)
    description_next_week = models.TextField(max_length=1000, default='', null=True)
    description_comment = models.TextField(max_length=1000, default='', null=True)
    description_summary = models.TextField(max_length=1000, default='', null=True)

    def __str__(self):
        return f'week-{self.week} project-{self.task.name} Task-{self.task.project.name} user-{self.task_creator.profileinfo.office_id_no}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
