from django.db import models
from home.models import Department
from django.contrib.auth.models import User
import datetime
from colorfield.fields import ColorField


class RequisitionInfo(models.Model):
    name = models.CharField(max_length=1000, default='')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)