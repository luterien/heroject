from apps.projects.models import Task, Project
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def update_task_status(request):
    is_done = request.GET.get('is_done')
    task_id = request.GET.get('task_id')

    status = True if is_done=="1" else False

    try:
        task = Task.objects.get(id=int(task_id))
    except Task.DoesNotExist:
        task = None

    if task:
        task.is_done = status
        task.save()

    result = {'is_done': is_done}

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def active_tasks(request, slug, template="projects/active_tasks.html"):
    prj = get_object_or_404(Project, slug=slug)
    ctx = {'project':prj}
    return render_to_response(template, ctx, context_instance = RequestContext(request))

def completed_tasks(request, slug, template="projects/completed_tasks.html"):
    prj = get_object_or_404(Project, slug=slug)
    ctx = {'project':prj}
    return render_to_response(template, ctx, context_instance = RequestContext(request))
