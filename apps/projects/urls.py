from django.conf.urls.defaults import *
from apps.projects.views import *
from apps.projects.ajax import *

urlpatterns = patterns('apps.projects.views',

    url(r'^create/$', create_project, name="create_project"),

    url(r'^(?P<slug>[-\w]+)/$', project_details, name="project_details"),
    url(r'^update/(?P<pk>\d+)/$', UpdateProject.as_view(), name='update_project'),

    # discussion urls
    url(r'^discussions/(?P<slug>[-\w\d]+)/$', discussion_details, name="discussion_details"),
    url(r'^(?P<project_id>[-\d]+)/discussions/create/$', CreateDiscussion.as_view(), name="create_discussion"),

    # task
    url(r'^(?P<project_id>[-\d]+)/task/create/$', CreateTask.as_view(), name="create_task"),
    url(r'^tasks/(?P<pk>[-\d]+)/$', task_details, name="task_details"),
    url(r'^tasks/update_status/$', update_task_status, name="update_task_status"),
    
    url(r'^tasks/(?P<task_id>[-\d]+)/comments/', CreateTaskComment.as_view(), name="create_task_comment"),

    url(r'^(?P<slug>[-\w]+)/completed_tasks/$', completed_tasks, name="completed_tasks"),
    url(r'^(?P<slug>[-\w]+)/active_tasks/$', active_tasks, name="active_tasks"),

    # post urls
    url(r'^discussion/(?P<discussion_id>[-\d]+)/post/create/$', CreateDiscussionComment.as_view(), name="create_post"),
 
)

