from django.shortcuts import render
from home.models import ProfileInfo, Department
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.contrib.auth.models import User
from django.core import serializers
from .models import (
    Tag, Team, VendorSupervisor,
    Vendor, ProjectInfo, Status, WeeklyUpdate
)
from home.models import Role


@login_required
def project_management(request):
    departments = Department.objects.all()
    teams = Team.objects.all()
    tags = Tag.objects.all()
    try:
        ulka_supervisors = User.objects.filter(profileinfo__role=Role.objects.get(name='Supervisor'))
        pms = User.objects.filter(profileinfo__role=Role.objects.get(name='PM'))
        managers = User.objects.filter(profileinfo__role=Role.objects.get(name='Manager'))
        ack_pers = pms = User.objects.all()
    except:
        ulka_supervisors = []
        pms = []
        managers = []
        ack_pers = []
    vendors = Vendor.objects.all()
    vendor_supervisors = VendorSupervisor.objects.all()
    members = ProfileInfo.objects.all()
    statuses = Status.objects.all().order_by('id')

    user_teams = Team.objects.filter(members=request.user)
    project_counts_c1 = {
        'All': len(ProjectInfo.objects.filter(members=request.user))
    }
    project_counts_c2 = {}
    for i, status in enumerate(statuses):
        if i < 2:
            project_counts_c1[status.name] = len(ProjectInfo.objects.filter(members=request.user).filter(status=status))
        else:
            project_counts_c2[status.name] = len(ProjectInfo.objects.filter(members=request.user).filter(status=status))

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
        "pms": pms,
        "managers": managers,
        "ack_pers": ack_pers,
        "vendors": vendors,
        "vendor_supervisors": vendor_supervisors,
        "members": members,
        "projects_1": projects_1,
        "project_rest": projects_rest,
        "today": datetime.date.today,
        "statuses": statuses,
        "user_teams": user_teams,
        "project_counts_c1": project_counts_c1,
        "project_counts_c2": project_counts_c2
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
        pms = request.POST.getlist('pms', None)
        managers = request.POST.getlist('managers', None)
        ulka_supervisors = request.POST.getlist('ulka_supervisors', None)
        ack_pers = request.POST.getlist('ack_pers', None)
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

            try:
                instance.vendor = Vendor.objects.get(name=vendor)
            except:
                pass
            instance.start_date = parse_date(start_date)
            instance.deadline = parse_date(end_date)
            instance.created_by = request.user
            instance.status = Status.objects.get(name="Pending")

            instance.project_id = f'{datetime.datetime.now().year}{str(instance.id).zfill(8)}'
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

            try:
                for v_s in vendor_supervisors:
                    instance.vendor_supervisors.add(VendorSupervisor.objects.filter(vendor=instance.vendor).get(
                        name=v_s.split('(')[0].strip()
                    ))
            except:
                pass

            for pm in pms:
                instance.vendor_supervisors.add(ProfileInfo.objects.get(
                    office_id_no=pm.split('(')[-1].replace(')', '')).user)

            for manager in managers:
                instance.vendor_supervisors.add(ProfileInfo.objects.get(
                    office_id_no=manager.split('(')[-1].replace(')', '')).user)

            for ack_per in ack_pers:
                instance.vendor_supervisors.add(ProfileInfo.objects.get(
                    office_id_no=ack_per.split('(')[-1].replace(')', '')).user)

            for ulka_supervisor in ulka_supervisors:
                instance.vendor_supervisors.add(ProfileInfo.objects.get(
                    office_id_no=ulka_supervisor.split('(')[-1].replace(')', '')).user)

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
            project=proj).filter(creator=request.user).filter(~Q(week=week_number)).values()[:10:-1]
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

        query = WeeklyUpdate.objects.filter(
            project=proj).filter(creator=request.user).filter(week=week_number)
        if query.exists():
            instance = WeeklyUpdate.objects.filter(
                project=proj).filter(creator=request.user).get(
                week=week_number)
        else:
            instance = WeeklyUpdate()
        instance.week = week_number
        instance.created_at = datetime.datetime.now()
        instance.project = proj
        instance.creator = request.user
        instance.creator_pp_url = request.user.profileinfo.profile_picture_url
        instance.description_this_week = this_week
        instance.description_next_week = next_week
        instance.description_comment = comment
        if query.exists():
            instance.save(update_fields=['week', 'created_at', 'project', 'description_this_week',
                                         'description_next_week', 'description_comment'])
        else:
            instance.save()

        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


def set_project_progress(request):
    if request.method == "POST" and is_ajax(request=request):
        proj = ProjectInfo.objects.get(id=int(request.POST.get('proj_id', None)))
        proj.progress = int(request.POST.get('progress', None))
        proj.save(
            update_fields=['progress']
        )
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


def set_project_status(request):
    if request.method == "POST" and is_ajax(request=request):
        proj = ProjectInfo.objects.get(id=int(request.POST.get('proj_id', None)))
        proj.status = Status.objects.get(name=request.POST.get('status', None))
        proj.save(
            update_fields=['status']
        )
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


@csrf_exempt
def create_teams(request):
    if request.method == "POST":
        user_not_found = []
        try:
            name = request.POST.get('Team', None)
            dept = request.POST.get('Department', None)

            print(name, dept)

            instance = Team()
            instance.name = name
            instance.department = Department.objects.get(name=dept)
            instance.save()

            members = request.POST.getlist('Members', None)

            for member in members:
                try:
                    instance.members.add(ProfileInfo.objects.get(office_id_no=member).user)
                except Exception as e:
                    user_not_found.append(member)

            return JsonResponse({"success": True, "not_found": user_not_found}, status=200)
        except Exception as e:
            return JsonResponse({"success": False}, status=200)
    return JsonResponse({"success": False}, status=200)
