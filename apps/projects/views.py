from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse
from apps.actions.forms import *
from apps.projects.forms import *
from apps.actions.utils import action, start_following
from apps.profiles.models import Profile


# check if the current user has access to project
def _has_project_access(request, project):
    return project in request.user.projects


@login_required
def project_details(request, slug, template="projects/project_details.html"):
    project = get_object_or_404(Project, slug=slug)

    invitation_form = InvitationForm()
    invitation_form.fields['receiver'].queryset = Profile.objects.exclude(
        id__in=project.people.values_list('id', flat=True))

    ctx = {'project': project,
           'new_task_form': CreateTaskForm,
           'projects': request.user.projects,
           'project_invitation_form': invitation_form}

    if not _has_project_access(request, project):
        return redirect('index')

    return render(request, template, ctx)


@login_required
def task_details(request, pk, template="projects/task_details.html"):
    task = get_object_or_404(Task, pk=pk)
    
    ctx = {'task': task,
           'task_comment_form': CreateTaskCommentForm}

    if not _has_project_access(request, task.project):
        return redirect('index')

    return render(request, template, ctx)


@login_required
def discussion_details(request, slug,
                       template="projects/discussion_details.html"):
    discussion = get_object_or_404(Discussion, slug=slug)
    ctx = {'discussion': discussion,
           'new_post_form': CreateDiscussionCommentForm}
    if not _has_project_access(request, discussion.project):
        return redirect('index')

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
                action(request.user, prj, "create")
            
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
        return reverse('update_project', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        _get = super(UpdateProject, self).get(request, *args, **kwargs)
        if not _has_project_access(request, self.object):
            return redirect('index')
        return _get


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
        action(self.request.user, self.object, "create", self.object.project)
        start_following(self.request.user, self.object)
        return super(CreateDiscussion, self).form_valid(form)


class CreateDiscussionComment(CreateView):
    template_name = "create_post.html"
    model = DiscussionComment
    form_class = CreateDiscussionCommentForm

    def get_success_url(self):
        return reverse('discussion_details',
                       kwargs={'slug': self.object.discussion.slug})

    def form_valid(self, form):
        self.object = form.instance
        self.object.discussion_id = self.kwargs['discussion_id']
        # started by
        self.object.started_by = self.request.user
        self.object.save()
        # create an action
        # will be celery task
        action(self.request.user, self.object,
               "comment", self.object.discussion)
        return super(CreateDiscussionComment, self).form_valid(form)


class CreateTask(CreateView):
    template_name = "create_task.html"
    model = Task
    form_class = CreateTaskForm

    def get_success_url(self):
        prj = Project.objects.get(id=self.kwargs["project_id"])
        return reverse('project_details', kwargs={'slug': prj.slug})

    def form_valid(self, form):
        self.object = form.instance
        self.object.project_id = self.kwargs['project_id']
        # started by
        self.object.started_by = self.request.user
        self.object.ordering = 1 # temporary fix
        self.object.save()
        # create an action
        # will be celery task
        action(self.request.user, self.object, "create", self.object.project)
        return super(CreateTask, self).form_valid(form)


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
        action(self.request.user, self.object, "comment", self.object.task)
        return super(CreateTaskComment, self).form_valid(form)
