from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from apps.projects.views import project_details, task_details, discussion_details, todo_details, discussion_list
from apps.profiles.views import profile_details, organization_details, login_user, register_user, logout_user, index

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectbonus.views.home', name='home'),
    # url(r'^projectbonus/', include('projectbonus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$',                              direct_to_template, {'template': 'home/index.html'}),

    # Profile urls
    url(r'^$',                                      login_user,         name="login"),
    url(r'^register/$',                             register_user,      name="register"),
    url(r'^logout/$',                               logout_user,        name="logout"),
    url(r'^profile/$',                              profile_details,    name="profile_details"),
    url(r'^index/$',                                index,              name="index"),


    # Project urls
    url(r'^project/([-\d]+)/([-\w]+)/$',            project_details,    name="project_details"),
    url(r'^project/discussion/([-\d]+)/([-\w]+)/$', discussion_details, name="discussion_details"),
    url(r'^project/todo/([-\d]+)/([-\w]+)/$',       todo_details,       name="todo_details"),
    #url(r'', 'discussion_list'),
    #url(r'', 'organization_details'),
    #url(r'', 'todo_details'),
)
