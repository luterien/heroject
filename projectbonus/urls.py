from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from apps.profiles.views import *
from apps.profiles.ajax import *
from apps.actions.views import *
from django.contrib import admin

admin.autodiscover()

## TODO
## fix indentation + make seperate urls.py's for each app

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^project/', include('apps.projects.urls')),

    url(r'^profile/', include('apps.profiles.urls')),

    url(r'^about/', TemplateView.as_view(template_name="about.html")),

    url(r'^contact/', TemplateView.as_view(template_name="contact.html")),

    # profile urls
    url(r'^$', login_user, name="login"),

    url(r'^register/$', register_user, name="register"),

    url(r'^logout/$', logout_user, name="logout"),

    url(r'^index/$', index, name="index"),

    url(r'^organization/create/$', CreateOrganization.as_view(),
        name="create_organization"),

    url(r'^organization/(?P<slug>[-\w]+)/$', OrganizationDetails.as_view(),
        name="organization_details"),

    url(r'^organization/(?P<organization_id>[-\d]+)/invite/',
        InviteToOrganization.as_view(), name="invite_to_organization"),

    url(r'^organization/(?P<slug>[-\w]+)/update/$',
        OrganizationUpdate.as_view(), name="update_organization"),

    url(r'^project/(?P<project_id>[-\d]+)/invite/$',
        InviteToProject.as_view(), name="invite_to_project"),

    url(r'^task/assign/$', assign_user, name="assign_user"),

    url(r'^task/remove/$', remove_user, name="remove_user"),

    url(r'task/(?P<task_id>[-\d]+)/people/', task_people, name="task_people"),

)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )