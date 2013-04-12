from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

ORG_CHOICES = (
        ('', ''),
        ('', '')
    )


class Organization(models.Model):
    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    org_type = models.CharField(_("Organization Type"), max_length=60, choices=ORG_CHOICES)

    people = models.ManyToManyField('Profile', verbose_name=(u"People"))

    def __unicode__(self):
        return u"%s" % (self.user)

    def get_absolute_url(self):
        pass


class ProfileManager(models.Manager):
    def from_request(self, request, *args, **kwargs):
        try:
            usr = self.get(user=request.user)
        except:
            usr = None

        return usr

class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))

    birthdate = models.DateTimeField(_("Birth Date"), null=True, blank=True)

    picture = models.ImageField(("Profile Picture"), upload_to="/users/avatars/", null=True, blank=True)

    objects = ProfileManager()

    def __unicode__(self):
        return u"%s" % (self.user)

    def get_absolute_url(self):
        return reverse('profile_details')

    @property
    def projects(self):
        """ return the list of projects this user is a member of """
        return self.project_set.all()

    @property
    def tasks(self):
    	""" return the list of Task objects which are assigned to the user """
    	pass