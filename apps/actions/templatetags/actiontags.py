from django import template
from django.contrib.contenttypes.models import ContentType

from apps.actions.models import Action
from apps.projects.models import TaskComment

register = template.Library()


@register.assignment_tag
def get_actions(obj):
    """
    Return the actions performed on the given object
    """
    ct = ContentType.objects.get_for_model(obj.__class__)

    return Action.objects.filter(target_content_type=ct,
                                 target_object_id=obj.id)


@register.filter
def of_type(obj, type):
    """ under construction """
    
    TYPE_MAP = {
        'taskcomment': TaskComment,
    }
    
    return isinstance(obj, TYPE_MAP.get(type))
    
    
