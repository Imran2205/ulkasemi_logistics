from django.shortcuts import render


def project_management(request):
    context = {

    }
    return render(request, 'project_management/index.html', context)

