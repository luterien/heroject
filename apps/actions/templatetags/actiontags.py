from django import template
from django.contrib.contenttypes.models import ContentType

from apps.actions.models import Action

register = template.Library()

@register.assignment_tag
def get_actions(obj):
    """ Return the actions performed on the given object """
    ct = ContentType.objects.get_for_model(obj.__class__)

    return Action.objects.filter(target_content_type=ct, target_object_id=obj.id)



