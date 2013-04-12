from apps.projects.models import *
from django.shortcuts import render, get_object_or_404
from apps.utils import get_or_none
from django.contrib.auth.decorators import login_required

@login_required
def project_details(request, pk, slug, template="projects/project_details.html"):
    project = get_object_or_404(Project, pk=pk, slug=slug)
    ctx = {'project':project}
    return render(request, template, ctx)

@login_required
def task_details(request, pk, slug, template=""):
	task = get_or_none(Task, {'pk':pk, 'slug':slug})

	ctx = {'task':task}

	return render(request, template, ctx)

@login_required
def discussion_details(request, pk, slug, template="projects/discussion_details.html"):
	discussion = get_object_or_404(Discussion, pk=pk, slug=slug)

	ctx = {'discussion':discussion}

	return render(request, template, ctx)

@login_required
def todo_details(request, pk, slug, template="projects/todo_details.html"):
	""" returns the list of todo lists for the given project"""
	todo = get_object_or_404(ToDoList, pk=pk, slug=slug)

	ctx = {'todo':todo}

	return render(request, template, ctx)

@login_required
def discussion_list(request, template=""):
	""" returns the list of discussions for the given project"""
	pass

