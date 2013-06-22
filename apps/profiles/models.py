from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager

from projectbonus.utils import slugify
from apps.profiles.tasks import make_square


class Profile(AbstractUser):

    birthdate = models.DateTimeField(_("Birth Date"),
                                     null=True, blank=True)

    picture = models.ImageField(_("Profile Picture"),
                                upload_to="users/avatars/",
                                null=True, blank=True)


    def __unicode__(self):
        return u"%s" % self.username

    @models.permalink
    def get_absolute_url(self):
        return ('profile_details', (), {})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.picture:
            make_square(self.picture.path)

    @property
    def projects(self):
        """ return the list of projects this user is a member of """
        return self.project_set.all()

    @property
    def tasks(self):
        """ return the list of Task objects which are assigned to the user """
        return self.task_set.all()

    @property
    def unread_notifications(self):
        return self.received_notifications.filter(is_read=False)

    @property
    def read_notifications(self):
        return self.received_notifications.filter(is_read=True)

    @property
    def invitations_received(self):
        return self.received_invitations.all()

    @property
    def invitations_sent(self):
        pass

    @property
    def follows(self, obj):
        pass




