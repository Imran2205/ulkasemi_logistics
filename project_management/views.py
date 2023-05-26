from django.shortcuts import render
from home.models import ProfileInfo, Department
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.core import serializers
from .models import (
    Tag, Team, UlkaSupervisor, VendorSupervisor,
    Vendor, ProjectInfo, Status, WeeklyUpdate
)
from allauth.socialaccount.models import SocialAccount


@login_required
def project_management(request):
    departments = Department.objects.all()
    teams = Team.objects.all()
    tags = Tag.objects.all()
    ulka_supervisors = UlkaSupervisor.objects.all()
    vendors = Vendor.objects.all()
    vendor_supervisors = VendorSupervisor.objects.all()
    members = ProfileInfo.objects.all()
    statuses = Status.objects.all()

    cond1 = Q(members=request.user)
    # cond2 = Q(ulka_supervisors=request.user)
    cond3 = Q(created_by=request.user)
    projects = ProjectInfo.objects.filter(cond1 | cond3).order_by('deadline').distinct()
    if len(projects) > 1:
        projects_1 = projects[:1]
        projects_rest = projects[1:]
    elif len(projects) == 1:
        projects_1 = projects
        projects_rest = []
    else:
        projects_1 = []
        projects_rest = []

    context = {
        "departments": departments,
        "teams": teams,
        "tags": tags,
        "ulka_supervisors": ulka_supervisors,
        "vendors": vendors,
        "vendor_supervisors": vendor_supervisors,
        "members": members,
        "projects_1": projects_1,
        "project_rest": projects_rest,
        "today": datetime.date.today,
        "statuses": statuses
    }
    return render(request, 'project_management/index.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
# @csrf_exempt
def ajax_create_project(request):
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
            instance.created_by = request.user
            instance.status = Status.objects.get(name="Pending")

            instance.project_id = str(instance.id).zfill(8)
            instance.save(update_fields=[
                'project_id', 'vendor', 'start_date', 'deadline', 'entry_date', 'status', 'created_by'
            ])

            for tag in tags:
                instance.tags.add(Tag.objects.get(name=tag))

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


@login_required
def ajax_get_proj(request, pk):
    if request.method == "GET" and is_ajax(request=request):
        proj = ProjectInfo.objects.get(id=pk)

        week_number = datetime.datetime.now().isocalendar()[1]

        updates_others = WeeklyUpdate.objects.filter(
            project=proj).filter(creator=request.user).filter(~Q(week=week_number)).values()
        updates_this_week = WeeklyUpdate.objects.filter(
            project=proj).filter(creator=request.user).filter(week=week_number).values()

        context = {
            'proj_name': proj.name,
            'proj_desc': proj.description,
            'proj_progress': proj.progress,
            'proj_status': proj.status.name,
            'updates_this_week': list(updates_this_week),
            'updates_others': list(updates_others)
        }
        return JsonResponse(data=context, status=200, safe=False)
    return JsonResponse({}, status=400)


@login_required
def ajax_post_update(request, pk):
    if request.method == "POST" and is_ajax(request=request):
        proj = ProjectInfo.objects.get(id=pk)
        this_week = request.POST.get('this_week', None)
        next_week = request.POST.get('next_week', None)
        comment = request.POST.get('comment', None)

        week_number = datetime.datetime.now().isocalendar()[1]

        state = ['c', 'c', 'c']

        if this_week:
            query = WeeklyUpdate.objects.filter(
                project=proj).filter(creator=request.user).filter(week=week_number).filter(type='this_week')
            if query.exists():
                instance = WeeklyUpdate.objects.filter(
                    project=proj).filter(creator=request.user).filter(
                    week=week_number).get(type='this_week')
            else:
                instance = WeeklyUpdate()
            instance.week = week_number
            instance.created_at = datetime.datetime.now()
            instance.project = proj
            instance.creator = request.user
            instance.type = 'this_week'
            instance.description = this_week
            if query.exists():
                instance.save(update_fields=['week', 'created_at', 'project', 'type', 'description'])
                state[0] = 'u'
            else:
                instance.save()
        if next_week:
            query = WeeklyUpdate.objects.filter(
                project=proj).filter(creator=request.user).filter(week=week_number).filter(type='next_week')
            if query.exists():
                instance = WeeklyUpdate.objects.filter(
                    project=proj).filter(creator=request.user).filter(
                    week=week_number).get(type='next_week')
            else:
                instance = WeeklyUpdate()
            instance.week = week_number
            instance.created_at = datetime.datetime.now()
            instance.project = proj
            instance.creator = request.user
            instance.type = 'next_week'
            instance.description = next_week
            if query.exists():
                instance.save(update_fields=['week', 'created_at', 'project', 'type', 'description'])
                state[1] = 'u'
            else:
                instance.save()

        if comment:
            query = WeeklyUpdate.objects.filter(
                project=proj).filter(creator=request.user).filter(week=week_number).filter(type='comment')
            if query.exists():
                instance = WeeklyUpdate.objects.filter(
                    project=proj).filter(creator=request.user).filter(
                    week=week_number).get(type='comment')
            else:
                instance = WeeklyUpdate()
            instance.week = week_number
            instance.created_at = datetime.datetime.now()
            instance.project = proj
            instance.creator = request.user
            instance.type = 'comment'
            instance.description = comment
            if query.exists():
                instance.save(update_fields=['week', 'created_at', 'project', 'type', 'description'])
                state[2] = 'u'
            else:
                instance.save()

        return JsonResponse({"success": True, "state": state}, status=200)
    return JsonResponse({"success": False}, status=400)
