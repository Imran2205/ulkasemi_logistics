from django.contrib import admin
from .models import (
    Team, Leave, Tag, Status, Vendor, VendorSupervisor,
    ProjectInfo, WeeklyUpdate, TaskInfo, WeeklyUpdateTask,
    TaskSuppFile
)

admin.site.register(Team)
admin.site.register(Leave)
admin.site.register(Tag)
admin.site.register(Status)
admin.site.register(Vendor)
admin.site.register(VendorSupervisor)
admin.site.register(ProjectInfo)
admin.site.register(WeeklyUpdate)
admin.site.register(TaskInfo)
admin.site.register(WeeklyUpdateTask)
admin.site.register(TaskSuppFile)
