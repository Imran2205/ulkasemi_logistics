from django.shortcuts import render
from home.models import ProfileInfo, Department
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import (
    Tag, Team, UlkaSupervisor, VendorSupervisor,
    Vendor, ProjectInfo
)


def project_management(request):
    departments = Department.objects.all()
    teams = Team.objects.all()
    tags = Tag.objects.all()
    ulka_supervisors = UlkaSupervisor.objects.all()
    vendors = Vendor.objects.all()
    vendor_supervisors = VendorSupervisor.objects.all()
    members = ProfileInfo.objects.all()
    context = {
        "departments": departments,
        "teams": teams,
        "tags": tags,
        "ulka_supervisors": ulka_supervisors,
        "vendors": vendors,
        "vendor_supervisors": vendor_supervisors,
        "members": members
    }
    return render(request, 'project_management/index.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def ajax_create_project(request):
    current_user = request.user
    if request.method == "POST" and is_ajax(request=request):
        project_name = request.POST.get('project_name', None)
        project_description = request.POST.get('project_description', None)
        members = request.POST.getlist('members', None)
        departments = request.POST.getlist('departments', None)
        teams = request.POST.getlist('teams', None)
        vendor = request.POST.get('vendor', None)
        vendor_supervisors = request.POST.getlist('vendor_supervisors', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        tags = request.POST.getlist('tags', None)

        # print(
        #     project_name,
        #     project_description,
        #     members,
        #     departments,
        #     teams,
        #     vendor,
        #     vendor_supervisors,
        #     start_date,
        #     end_date,
        #     tags
        # )

        try:
            instance = ProjectInfo()
            instance.name = project_name
            instance.description = project_description
            instance.progress = 0
            instance.save()

            instance.vendor = Vendor.objects.get(name=vendor)
            instance.start_date = parse_date(start_date)
            instance.deadline = parse_date(end_date)

            for tag in tags:
                instance.tags.add(Tag.objects.get(name=tag))

            instance.project_id = str(instance.id).zfill(8)
            instance.save(update_fields=[
                'project_id', 'vendor', 'start_date', 'deadline', 'entry_date'
            ])

            for member in members:
                instance.members.add(ProfileInfo.objects.get(office_id_no=member.split('(')[-1].replace(')', '')).user)
            for dept in departments:
                instance.departments.add(Department.objects.get(name=dept))
            for team in teams:
                instance.teams.add(Team.objects.get(name=team))

            for v_s in vendor_supervisors:
                instance.vendor_supervisors.add(VendorSupervisor.objects.filter(vendor=instance.vendor).get(
                    name=v_s.split('(')[0].strip()
                ))
        except Exception as e:
            return JsonResponse({"success": False, "error": e}, status=400)
        return JsonResponse({}, status=200)
    return JsonResponse({"success": False}, status=400)

