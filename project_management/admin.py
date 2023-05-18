from django.contrib import admin
from .models import (
    Team, Leave, UlkaSupervisor, Tag, Status, Vendor, VendorSupervisor,
    ProjectInfo, WeeklyUpdate
)

admin.site.register(Team)
admin.site.register(Leave)
admin.site.register(UlkaSupervisor)
admin.site.register(Tag)
admin.site.register(Status)
admin.site.register(Vendor)
admin.site.register(VendorSupervisor)
admin.site.register(ProjectInfo)
admin.site.register(WeeklyUpdate)
