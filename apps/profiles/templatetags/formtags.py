from apps.profiles.forms import InvitationForm
from django import template

register = template.Library()

@register.assignment_tag(takes_context=True)
def invitation_form(context):
	return InvitationForm()

