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


color_dict = {
    "1": "fb8500ff",
    "2": "ffb703ff",
    "3": "219ebcff",
    "4": "d4a373ff",
    "5": "ccd5aeff",
    "6": "606c38ff",
    "7": "bc6c25ff",
    "8": "dda15eff",
    "9": "fb5607ff",
    "10": "8338ecff",
    "11": "2a9d8fff",
    "12": "e76f51ff",
    "13": "588157ff",
    "14": "d5bdafff",
    "15": "0096c7ff",
    "16": "00b4d8ff",
    "17": "a8dadcff",
    "18": "457b9dff",
    "19": "4a4e69ff",
    "20": "118ab2ff",
    "21": "00afb9ff",
    "22": "0081a7ff",
    "23": "fca311ff",
    "24": "84a59dff",
    "25": "f6bd60ff",
    "26": "9f86c0ff",
    "27": "e4c1f9ff",
    "28": "006d77ff",
    "29": "00b4d8ff",
    "30": "e09f3eff",
    "31": "0fa3b1ff",
    "32": "eddea4ff",
    "33": "f7a072ff",
    "34": "31572cff",
    "35": "4f772dff",
    "36": "cb997eff",
    "37": "6b705cff",
    "38": "ff8fabff",
    "39": "fb6f92ff",
    "40": "7209b7ff",
    "41": "a3a380ff",
    "42": "cbf3f0ff",
    "43": "2ec4b6ff",
    "44": "25a18eff",
    "45": "8ac926ff",
    "46": "6a4c93ff",
    "47": "dd6e42ff",
    "48": "c0d6dfff",
    "49": "5f0f40ff",
    "50": "c9cba3ff"
}


@login_required
def project_management(request):
    departments = Department.objects.all()
    teams = Team.objects.all()
    tags = Tag.objects.all()
    try:
        ulka_supervisors = User.objects.filter(profileinfo__role=Role.objects.get(name='Supervisor'))
        pms = User.objects.filter(profileinfo__role=Role.objects.get(name='PM'))
        managers = User.objects.filter(profileinfo__role=Role.objects.get(name='Manager'))
        ack_pers = User.objects.filter(~Q(profileinfo__office_id_no="000000"))
    except:
        ulka_supervisors = []
        pms = []
        managers = []
        ack_pers = []
    vendors = Vendor.objects.all()
    vendor_supervisors = VendorSupervisor.objects.all()
    members = User.objects.filter(~Q(profileinfo__office_id_no="000000"))
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
            search_value = ""
            instance = ProjectInfo()
            instance.name = project_name
            search_value = search_value + project_name
            instance.description = project_description
            search_value = search_value + project_description
            instance.progress = 0
            instance.save()

            try:
                instance.vendor = Vendor.objects.get(name=vendor)
                search_value = search_value + " " + vendor
            except:
                pass
            instance.start_date = parse_date(start_date)
            instance.deadline = parse_date(end_date)
            instance.created_by = request.user
            search_value = search_value + " " + request.user.first_name + " " + request.user.last_name + " " + \
                request.user.profileinfo.office_id_no
            instance.status = Status.objects.get(name="Pending")

            instance.project_id = f'{datetime.datetime.now().year}{str(instance.id).zfill(8)}'
            search_value = search_value + " " + instance.project_id
            instance.save(update_fields=[
                'project_id', 'vendor', 'start_date', 'deadline', 'entry_date', 'status', 'created_by'
            ])

            for tag in tags:
                try:
                    tag_obj = Tag.objects.get(name=tag)
                except:
                    tag_obj = Tag()
                    tag_obj.name = tag
                    tag.save()
                    prev_tag_id = tag.id - 1
                    try:
                        use_color = Tag.objects.get(id=prev_tag_id).last_used_color + 1
                    except:
                        use_color = 0

                    if use_color >= len(list(color_dict.keys())):
                        use_color = 0

                    tag.last_used_color = use_color
                    tag.color = color_dict[str(use_color)]
                    tag.save(
                        update_fields=['color', 'last_used_color']
                    )

                instance.tags.add(tag_obj)
                search_value = search_value + " " + tag_obj.name

            for member in members:
                instance.members.add(ProfileInfo.objects.get(office_id_no=member.split('(')[-1].replace(')', '')).user)
            for dept in departments:
                instance.departments.add(Department.objects.get(name=dept))
                search_value = search_value + " " + dept
            for team in teams:
                instance.teams.add(Team.objects.get(name=team))
                search_value = search_value + " " + team

            try:
                for v_s in vendor_supervisors:
                    instance.vendor_supervisors.add(VendorSupervisor.objects.filter(vendor=instance.vendor).get(
                        name=v_s.split('(')[0].strip()
                    ))
                    search_value = search_value + " " + v_s.split('(')[0].strip()
            except:
                pass

            for pm in pms:
                instance.ulka_pm.add(ProfileInfo.objects.get(
                    office_id_no=pm.split('(')[-1].replace(')', '')).user)
                search_value = search_value + " " + pm.split('(')[-1].replace(')', '')

            for manager in managers:
                instance.ulka_manager.add(ProfileInfo.objects.get(
                    office_id_no=manager.split('(')[-1].replace(')', '')).user)
                search_value = search_value + " " + manager.split('(')[-1].replace(')', '')

            for ack_per in ack_pers:
                instance.ulka_ack_person.add(ProfileInfo.objects.get(
                    office_id_no=ack_per.split('(')[-1].replace(')', '')).user)
                search_value = search_value + " " + ack_per.split('(')[-1].replace(')', '')

            for ulka_supervisor in ulka_supervisors:
                instance.ulka_supervisors.add(ProfileInfo.objects.get(
                    office_id_no=ulka_supervisor.split('(')[-1].replace(')', '')).user)
                search_value = search_value + " " + ulka_supervisor.split('(')[-1].replace(')', '')

            instance.search_field = search_value

            instance.save(
                update_fields=['search_field']
            )

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


def get_user_pop_up_info(request,):
    if request.method == "GET" and is_ajax(request=request):
        print(request.GET.get('id', None))
        user = User.objects.get(id=int(request.GET.get('id', None)))
        name = f'{user.first_name} {user.last_name}'
        ulka_email = user.email
        gf_email = user.profileinfo.gf_email
        contact_no = user.profileinfo.contact_no
        designation = user.profileinfo.designation
        try:
            department = user.profileinfo.department.name
        except:
            department = 'N/A'
        profile_picture = user.profileinfo.profile_picture_url

        teams = Team.objects.filter(members=user).values()

        statuses = Status.objects.all().order_by('id')
        project_counts_c1 = {
            'All': len(ProjectInfo.objects.filter(members=user))
        }
        project_counts_c2 = {}
        for i, status in enumerate(statuses):
            if i < 2:
                project_counts_c1[status.name] = len(
                    ProjectInfo.objects.filter(members=user).filter(status=status))
            else:
                project_counts_c2[status.name] = len(
                    ProjectInfo.objects.filter(members=user).filter(status=status))

        context = {
            "name": name,
            "designation": designation,
            "ulka_email": ulka_email,
            "teams": list(teams),
            "project_counts_c1": project_counts_c1,
            "project_counts_c2": project_counts_c2,
            "profile_picture": profile_picture,
            "department": department,
            'gf_email': gf_email,
            'contact_no': contact_no
        }
        return JsonResponse(data=context, status=200, safe=False)
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


def set_user_info(request):
    if request.method == "POST":
        try:
            office_id = request.POST.get('ID', None)
            dept = request.POST.get('Department', None)
            designation = request.POST.get('Designation', None)
            username = request.POST.get('Username', None)
            phone = request.POST.get('Phone', None)
            gf_email = request.POST.get('GF Email', None)
            blood_group = request.POST.get('Blood Group', None)

            profile_instance = ProfileInfo.objects.get(office_id_no=office_id)
            user_instance = profile_instance.user

            profile_instance.designation = designation
            profile_instance.contact_no = phone
            profile_instance.gf_email = gf_email
            profile_instance.blood_group = blood_group
            profile_instance.department = Department.objects.get(name=dept)

            user_instance.username = username

            profile_instance.save(
                update_fields=['department', 'designation', 'gf_email', 'contact_no', 'blood_group']
            )
            user_instance.save(
                update_fields=['username']
            )

            return JsonResponse({"success": True}, status=200)
        except Exception as e:
            office_id = request.POST.get('ID', None)
            return JsonResponse({"success": False, "ID": office_id}, status=200)
    return JsonResponse({"success": False}, status=200)


@login_required
def ajax_set_active_time(request):
    if request.method == "POST" and is_ajax(request=request):
        time = request.POST.get('time', None)
        ofc_id = request.POST.get('id', None)
        instance = ProfileInfo.objects.get(office_id_no=ofc_id)
        instance.last_activity = time
        instance.save(
            update_fields=['last_activity']
        )
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=200)


@login_required
def ajax_get_active_time(request):
    if request.method == "GET" and is_ajax(request=request):
        ofc_id = request.GET.get('id', None)
        time = ProfileInfo.objects.get(office_id_no=ofc_id).last_activity
        return JsonResponse({"success": True, "time": time}, status=200)
    return JsonResponse({"success": False}, status=200)


@login_required
def ajax_search_project(request):
    if request.method == "GET" and is_ajax(request=request):
        ofc_id = request.GET.get('id', None)
        time = ProfileInfo.objects.get(office_id_no=ofc_id).last_activity
        return JsonResponse({"success": True, "time": time}, status=200)
    return JsonResponse({"success": False}, status=200)