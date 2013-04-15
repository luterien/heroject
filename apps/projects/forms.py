from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.projects.models import *
from apps.profiles.models import *



class NewProjectForm(forms.Form):
    title = forms.CharField(label=_("Project Title"))
    description = forms.CharField(label=_("Description"))


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', )


class CreateDiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'content', )


class CreateDiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ('title', 'content', )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',)


class CreateTaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', )

