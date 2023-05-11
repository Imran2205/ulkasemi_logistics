from django.db import models


class ProjectInfoModel(models.Model):
    project_name = models.CharField(max_length=1000, default='', unique=True)

