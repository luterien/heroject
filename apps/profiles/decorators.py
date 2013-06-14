from django.shortcuts import redirect
from functools import wraps


def anonymous_required(redirect_url=None):
    def decorator(function):
        def _control(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(redirect_url)
            else:
                return function(request, *args, **kwargs)
        return wraps(function)(_control)
    return decorator