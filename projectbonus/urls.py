from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from apps.projects.views import *
from apps.profiles.views import *
from apps.projects.ajax import update_task_status

from django.contrib import admin
admin.autodiscover()

## TODO
## i simply used random url names,fix them later

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectbonus.views.home', name='home'),
    # url(r'^projectbonus/', include('projectbonus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$',                              direct_to_template, {'template': 'home/index.html'}),

    # profile urls
    url(r'^$',                                           login_user,         name="login"),
    url(r'^register/$',                                  register_user,      name="register"),
    url(r'^logout/$',                                    logout_user,        name="logout"),
    url(r'^profile/$',                                   profile_details,    name="profile_details"),
    url(r'^index/$',                                     index,              name="index"),

    url(r'^organization/(?P<pk>[-\d]+)/$',             OrganizationDetails.as_view() , name="organization_details"),

    # project urls
    url(r'^project/(?P<slug>[-\w\d]+)/$',                  project_details,            name="project_details"),
    url(r'^project/create/$',                                           create_project,             name="create_project"),
    url(r'^project/update/(?P<pk>\d+)/$',                               UpdateProject.as_view(),    name='update_project'),

    # discussion urls
    url(r'^project/discussions/(?P<slug>[-\w\d]+)/$',      discussion_details,         name="discussion_details"),
    url(r'^project/(?P<project_id>[-\d]+)/discussions/create/$',        CreateDiscussion.as_view(), name="create_discussion"),

    # post urls
    url(r'^discussion/(?P<discussion_id>[-\d]+)/post/create/$',         CreateDiscussionComment.as_view(),    name="create_post"),
    #url(r'', 'discussion_list'),
    #url(r'', 'organization_details'),
    #url(r'', 'todo_details'),
    
    # task
    url(r'^project/(?P<project_id>[-\d]+)/task/create/$',               CreateTask.as_view(),         name="create_task"),
    url(r'^project/tasks/(?P<pk>[-\d]+)/$',                             task_details,                 name="task_details"),
    url(r'^tasks/update_status/$',                                      update_task_status,           name="update_task_status"),
    
    # task comment
    url(r'^project/tasks/(?P<task_id>[-\d]+)/comments/',                CreateTaskComment.as_view(),  name="create_task_comment"),

)
