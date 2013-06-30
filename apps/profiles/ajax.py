from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, get_object_or_404

from apps.projects.models import Task
from apps.profiles.models import Profile
from apps.actions.tasks import action

def assign_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    u = Profile.objects.get(id=int(user_id))
    t = Task.objects.get(id=int(task_id))

    if u in t.project.people.all() and u not in t.people.all():
        t.people.add(u)
        action.delay(request.user, u, "assigntotask", t)

    result = {'user_id': u.id, 'username': u.username}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def remove_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    p = Profile.objects.get(id=int(user_id))
    t = Task.objects.get(id=int(task_id))

    if p in t.project.people.all() and p in t.people.all():
        t.people.remove(p)
        action.delay(request.user, p, "removefromtask", t)
        
    result = {}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def task_people(request, task_id, template="projects/assigned_people.html"):
    task = get_object_or_404(Task, pk=task_id)
    ctx = {'task': task}
    return render(request, template, ctx)

