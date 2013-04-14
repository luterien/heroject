from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView, CreateView

from apps.utils import get_or_none
from apps.projects.forms import *
from apps.projects.models import *


def _has_project_access(request, project):
    profile = Profile.objects.from_request(request)
    return project in profile.projects


@login_required
def project_details(request, pk, slug, template="projects/project_details.html"):
    project = get_object_or_404(Project, pk=pk, slug=slug)
    ctx = {'project':project}
    if not _has_project_access(request, project):
        return HttpResponseRedirect(reverse('index'))

    return render(request, template, ctx)


@login_required
def task_details(request, pk,template="projects/task_details.html"):
    task = get_object_or_404(Task, pk=pk)
    ctx = {'task':task}
    if not _has_project_access(request, task.project):
        return HttpResponseRedirect(reverse('index'))

    return render(request, template, ctx)


@login_required
def discussion_details(request, pk, slug, template="projects/discussion_details.html"):
    discussion = get_object_or_404(Discussion, pk=pk, slug=slug)
    ctx = {'discussion':discussion}
    if not _has_project_access(request, discussion.project):
        return HttpResponseRedirect(reverse('index'))

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
            desc  = request.POST.get('description')

            profile = Profile.objects.from_request(request)

            if not profile:
                pass

            prj = Project(title=title, description=desc)
            prj.save()

            prj.people.add(profile)
            
            return HttpResponseRedirect(prj.get_absolute_url())

    else:
        form = NewProjectForm()

    ctx = {'form': form}

    return render_to_response(template, ctx, context_instance=RequestContext(request))


class UpdateProject(UpdateView):
    template_name = "edit_project.html"
    model = Project
    form_class = UpdateProjectForm
    
    def get_success_url(self):
        return reverse('update_project', kwargs={'pk':self.object.pk })

    def get(self, request, *args, **kwargs):
        _get = super(UpdateProject, self).get(request, *args, **kwargs)
        if not _has_project_access(request, self.object):
            return HttpResponseRedirect(reverse('index'))
        return _get


class CreateDiscussion(CreateView):
    template_name = "create_discussion.html"
    model = Discussion
    form_class = CreateDiscussionForm

    def form_valid(self, form):
        self.object = form.instance
        self.object.project_id = self.kwargs['project_id']
        # started by
        profile = Profile.objects.from_request(self.request)
        self.object.started_by = profile
        self.object.save()
        return super(CreateDiscussion, self).form_valid(form)


class CreateDiscussionComment(CreateView):
    template_name = "create_post.html"
    model = DiscussionComment


## TODO
## create the 'starter post' when a discussion is created 

