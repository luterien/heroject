from django import forms
from apps.projects.models import Project
from django.utils.translation import ugettext_lazy as _

class NewProjectForm(forms.Form):
	title = forms.CharField(label=_("Project Title"))
	description = forms.CharField(label=_("Description"))


class EditProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('title', 'description', )

