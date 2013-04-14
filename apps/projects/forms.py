from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.projects.models import *
from apps.profiles.models import *

## TODO
## continue later

class NewProjectForm(forms.Form):
    title = forms.CharField(label=_("Project Title"))
    description = forms.CharField(label=_("Description"))


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        #fields = ('title', 'description', )

class CreateDiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'content', )

