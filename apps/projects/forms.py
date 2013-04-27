from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.projects.models import *
from apps.profiles.models import *



class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', )


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

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)

        self.fields['title'].required = True

class CreateTaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', )

