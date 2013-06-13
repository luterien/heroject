
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, get_object_or_404
from apps.projects.models import Task


def assign_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    u = User.objects.get(id=int(user_id))
    t = Task.objects.get(id=int(task_id))

    if u in t.project.people.all() and u not in t.people.all():
        t.people.add(u)

    result = {}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def remove_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    p = User.objects.get(id=int(user_id))
    t = Task.objects.get(id=int(task_id))

    if p in t.project.people.all() and p in t.people.all():
        t.people.remove(p)

    result = {}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def task_people(request, task_id, template="projects/assigned_people.html"):
    task = get_object_or_404(Task, pk=task_id)
    ctx = {'task': task}
    return render(request, template, ctx)

