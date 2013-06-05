from apps.projects.models import Task, Project
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.profiles.models import Profile

def assign_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    p=Profile.objects.get(id=int(user_id))
    t=Task.objects.get(id=int(task_id))

    if p in t.project.people.all() and p not in t.people.all():
        t.people.add(p)

    result = {}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def remove_user(request):
    user_id = request.GET.get('user_id')
    task_id = request.GET.get('task_id')

    p=Profile.objects.get(id=int(user_id))
    t=Task.objects.get(id=int(task_id))

    if p in t.project.people.all() and p in t.people.all():
        t.people.remove(p)

    result = {}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def task_people(request, task_id, template="projects/assigned_people.html"):
    task = get_object_or_404(Task, pk=task_id)
    ctx = {'task':task}
    return render_to_response(template, ctx, context_instance = RequestContext(request))