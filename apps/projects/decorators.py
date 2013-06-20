from django.shortcuts import redirect, get_object_or_404
from functools import wraps
from apps.projects.models import Task, Project, Discussion


def has_access_project(redirect_url=None, klass=None):
    def decorator(function):
        def _control(request, pk=None,  *args, **kwargs):
            if klass == Project:
                if kwargs.get('project_id'):
                    pk = kwargs.get('project_id')
                object = get_object_or_404(klass, pk=pk)
                if object not in request.user.projects:
                    return redirect(redirect_url)

            elif klass == Task or klass == Discussion:
                if kwargs.get('discussion_id'):
                    pk = kwargs.get('discussion_id')

                if kwargs.get('task_id'):
                    pk = kwargs.get('task_id')

                object = get_object_or_404(klass, pk=pk)
                if object.project not in request.user.projects:
                    return redirect(redirect_url)

            return function(request, pk, object, *args, **kwargs)
        return wraps(function)(_control)
    return decorator