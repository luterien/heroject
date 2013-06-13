from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change, password_change_done
from apps.profiles.views import *
from apps.actions.views import *

urlpatterns = patterns(
    'apps.profiles.views',

    url(r'^$', profile_details, name="profile_details"),

    url(r'^update/$', ProfileUpdate.as_view(), name="update_profile"),

    url(r'^update-password/$', password_change,
        {'template_name': 'profiles/update_password.html'},
        name="update_password"),

    url(r'^update-password/done/$', password_change_done,
        {'template_name': 'profiles/update_password_done.html'},
        name="password_change_done"),

    url(r'^invitations/$', invitations, name="invitations"),

    url(r'^invitations/(?P<id>[-\d]+)/$', reply_to_invitation, name="reply_to_invitation"),

    url(r'^notifications/$', notifications, name="notifications"),
)

