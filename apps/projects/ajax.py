from apps.projects.models import Task
from django.http import HttpResponse
from django.utils import simplejson

def update_task_status(request):
    is_done = request.GET.get('is_done')
    task_id = request.GET.get('task_id')

    try:
        task = Task.objects.get(id=int(task_id))
    except Task.DoesNotExist:
        task = None

    if task:
        task.is_done = (int(is_done) == 1)
        task.save()

    result = {'is_done': is_done}

    return HttpResponse(simplejson.dumps(result))