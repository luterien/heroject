from django.shortcuts import redirect
from functools import wraps
from apps.projects.models import Project


def anonymous_required(redirect_url=None):
    def decorator(function):
        def _control(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(redirect_url)
            else:
                return function(request, *args, **kwargs)
        return wraps(function)(_control)
    return decorator



def has_access_permission(cls=Project):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            
            item = cls._default_manager.get(**kwargs)

            if request.user in item.people.all():
                return function(request, *args, **kwargs)

            return redirect('index')

        return wraps(function)(_wrapped_view)
    return decorator
