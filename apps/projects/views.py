from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse

from apps.actions.forms import *
from apps.projects.forms import *
from apps.actions.tasks import action, start_following
from apps.profiles.models import Profile
from apps.projects.decorators import has_access_project


@login_required
@has_access_project('index', Project)
def project_details(request, pk, project):
    template = "projects/project_details.html"
    invitation_form = InvitationForm()
    invitation_form.fields['receiver'].queryset = Profile.objects.exclude(
        id__in=project.people.values_list('id', flat=True))

    ctx = {'project': project,
           'new_task_form': CreateTaskForm,
           'projects': request.user.projects,
           'project_invitation_form': invitation_form}

    return render(request, template, ctx)


@login_required
@has_access_project('index', Task)
def task_details(request, pk, task):
    template = "projects/task_details.html"
    ctx = {'task': task,
           'task_comment_form': CreateTaskCommentForm}

    return render(request, template, ctx)


@login_required
@has_access_project('index', Discussion)
def discussion_details(request, pk, discussion):
    template = "projects/discussion_details.html"
    ctx = {'discussion': discussion,
           'new_post_form': CreateDiscussionCommentForm}

    return render(request, template, ctx)


@login_required
def discussion_list(request, template=""):
    """ returns the list of discussions for the given project"""
    pass


@login_required
def create_project(request, template="new_project.html"):
    if request.method == "POST":
        form = NewProjectForm(request.POST)
        
        if form.is_valid():
            title = request.POST.get('title')
            desc = request.POST.get('description')

            prj = Project(title=title, description=desc)
            prj.save()

            prj.people.add(request.user)

            if prj:
                action.delay(request.user, prj, "create")
            
            return redirect(prj)

    else:
        form = NewProjectForm()

    ctx = {'form': form}

    return render(request, template, ctx)


class UpdateProject(UpdateView):
    template_name = "edit_project.html"
    model = Project
    form_class = UpdateProjectForm
    
    def get_success_url(self):
        return reverse('index')

    #use this decorator and method to optimum efficiency
    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Project))
    def dispatch(self, *args, **kwargs):
        return super(UpdateProject, self).dispatch(*args, **kwargs)


@login_required
@has_access_project('index', Project)
def delete_project(request, pk=None, project=None):
    project.delete()
    return redirect('index')


class CreateDiscussion(CreateView):
    template_name = "create_discussion.html"
    model = Discussion
    form_class = CreateDiscussionForm

    def form_valid(self, form):
        self.object = form.instance
        self.object.project_id = self.kwargs['project_id']
        # started by
        self.object.started_by = self.request.user
        self.object.save()
        # create an action
        # will be celery task
        action.delay(self.request.user, self.object, "create", self.object.project)
        start_following.delay(self.request.user, self.object)
        return super(CreateDiscussion, self).form_valid(form)

    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Project))
    def dispatch(self, *args, **kwargs):
        return super(CreateDiscussion, self).dispatch(*args, **kwargs)


class CreateDiscussionComment(CreateView):
    template_name = "create_post.html"
    model = DiscussionComment
    form_class = CreateDiscussionCommentForm

    def get_success_url(self):
        return reverse('discussion_details',
                       kwargs={'pk': self.object.discussion.id})

    def form_valid(self, form):
        self.object = form.instance
        self.object.discussion_id = self.kwargs['discussion_id']
        # started by
        self.object.started_by = self.request.user
        self.object.save()
        # create an action
        # will be celery task
        action.delay(self.request.user, self.object,
               "comment", self.object.discussion)
        return super(CreateDiscussionComment, self).form_valid(form)

    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Discussion))
    def dispatch(self, *args, **kwargs):
        return super(CreateDiscussionComment, self).dispatch(*args, **kwargs)


class CreateTask(CreateView):
    template_name = "create_task.html"
    model = Task
    form_class = CreateTaskForm

    def get_success_url(self):
        return reverse('project_details',
                       kwargs={'pk': self.kwargs["project_id"]})

    def form_valid(self, form):
        self.object = form.instance
        self.object.project_id = self.kwargs['project_id']
        # started by
        self.object.started_by = self.request.user
        self.object.ordering = 1  # temporary fix
        self.object.save()
        # create an action
        # will be celery task
        action.delay(self.request.user, self.object, "create", self.object.project)
        return super(CreateTask, self).form_valid(form)

    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Project))
    def dispatch(self, *args, **kwargs):
        return super(CreateTask, self).dispatch(*args, **kwargs)


class CreateTaskComment(CreateView):
    template_name = "create_task_comment.html"
    model = TaskComment
    form_class = CreateTaskCommentForm

    def get_success_url(self):
        prj = Task.objects.get(id=self.kwargs["task_id"])
        return reverse('task_details', kwargs={'pk': prj.pk})

    def form_valid(self, form):
        self.object = form.instance
        self.object.task_id = self.kwargs['task_id']
        # started by
        self.object.started_by = self.request.user
        self.object.save()
        # will be celery task
        # create an action
        action.delay(self.request.user, self.object, "comment", self.object.task)
        return super(CreateTaskComment, self).form_valid(form)

    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Task))
    def dispatch(self, *args, **kwargs):
        return super(CreateTaskComment, self).dispatch(*args, **kwargs)


class UpdateTask(UpdateView):
    template_name = "update_task.html"
    model = Task
    form_class = UpdateTaskForm

    def get_success_url(self):
        return reverse('project_details', kwargs={'pk': self.object.project.pk})

    #use this decorator and method to optimum efficiency
    @method_decorator(login_required())
    @method_decorator(has_access_project('index', Task))
    def dispatch(self, *args, **kwargs):
        return super(UpdateTask, self).dispatch(*args, **kwargs)


@login_required
@has_access_project('index', Task)
def delete_task(request, pk=None, task=None):
    task.delete()
    return redirect('project_details', pk=task.project.id)






























