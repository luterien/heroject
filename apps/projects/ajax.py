from apps.projects.models import Task, Project
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json


def update_task_status(request):
    is_done = request.GET.get('is_done')
    task_id = request.GET.get('task_id')

    status = True if is_done == "1" else False

    try:
        task = Task.objects.get(id=int(task_id))
    except Task.DoesNotExist:
        task = None

    if task:
        task.is_done = status
        task.save()

    result = {'is_done': is_done}

    return HttpResponse(json.dumps(result), mimetype="application/json")


def active_tasks(request, pk, template="projects/active_tasks.html"):
    prj = get_object_or_404(Project, pk=pk)
    ctx = {'project': prj}
    return render(request, template, ctx)


def completed_tasks(request, pk, template="projects/completed_tasks.html"):
    prj = get_object_or_404(Project, pk=pk)
    ctx = {'project': prj}
    return render(request, template, ctx)
