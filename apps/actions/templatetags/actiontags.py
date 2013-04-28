from django import template

from apps.actions.models import Action

register = template.Library()

@register.simple_tag(takes_context=True)
def actions_for_object(context, object):
	return Action.objects.filter(action_content_object=object)
