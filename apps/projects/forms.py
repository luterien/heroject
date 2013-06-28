from django import forms

from apps.projects.models import *


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', )

    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {"placeholder": "Project Name"}


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description',)


class CreateDiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('content', 'title',)


class CreateDiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ('content', )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['title'].widget.attrs = {"placeholder": "Task Title"}


class CreateTaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', )


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',)

