from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_change, password_change_done

from apps.projects.views import *
from apps.profiles.views import *
from apps.profiles.ajax import *
from apps.projects.ajax import *
from apps.actions.views import *

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

## TODO
## fix indentation + make seperate urls.py's for each app

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectbonus.views.home', name='home'),
    # url(r'^projectbonus/', include('projectbonus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^project/', include('apps.projects.urls')),

    url(r'^about/', direct_to_template, {'template':'about.html'}),
    url(r'^contact/', direct_to_template, {'template':'contact.html'}),

    # profile urls
    url(r'^$',                                           login_user,         name="login"),
    url(r'^register/$',                                  register_user,      name="register"),
    url(r'^logout/$',                                    logout_user,        name="logout"),
    url(r'^profile/$',                                   profile_details,    name="profile_details"),
    url(r'^index/$',                                     index,              name="index"),
    url(r'^profile/update/$',                            ProfileUpdate.as_view(), name="update_profile"),
    url(r'^profile/update-password/$',                   password_change,  
                {'template_name':'profiles/update_password.html'},  name="update_password"),
    url(r'^profile/update-password/done/$',              password_change_done, 
                {'template_name':'profiles/update_password_done.html'} , name="password_change_done"),

    url(r'^profile/invitations/$', invitations, name="invitations"),
    url(r'^profile/invitations/(?P<id>[-\d]+)/$', reply_to_invitation, name="reply_to_invitation"),

    url(r'^profile/notifications/$', notifications, name="notifications"),

    url(r'^organization/create/$',             CreateOrganization.as_view() , name="create_organization"),
    url(r'^organization/(?P<slug>[-\w]+)/$',             OrganizationDetails.as_view() , name="organization_details"),
    url(r'^organization/(?P<slug>[-\w]+)/update/$', OrganizationUpdate.as_view(), name="update_organization"),
    url(r'^organization/(?P<organization_id>[-\d]+)/invite/', InviteToOrganization.as_view() , name="invite_to_organization"),
    url(r'^project/(?P<project_id>[-\d]+)/invite/$', InviteToProject.as_view(), name="invite_to_project"),

    url(r'^task/assign/$', assign_user, name="assign_user"),
    url(r'^task/remove/$', remove_user, name="remove_user"),

    url(r'task/(?P<task_id>[-\d]+)/people/', task_people, name="task_people"),

)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )