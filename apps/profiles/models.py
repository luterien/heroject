from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.contrib.contenttypes import generic

from projectbonus.utils import slugify

ORG_CHOICES = (
        ('test', 'test'),
        ('', '')
    )


class Organization(models.Model):
    """
        Store organization details
    """
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField()

    description = models.TextField(_("Description"), null=True, blank=True)

    logo = models.ImageField(_('Logo'), upload_to="organizations/logos/", null=True, blank=True)

    org_type = models.CharField(_("Organization Type"), max_length=60, choices=ORG_CHOICES, null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    people = models.ManyToManyField('Profile', verbose_name=_("People"), related_name="organization_list", null=True, blank=True)

    admins = models.ManyToManyField('Profile', verbose_name=_("Admins"), null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ('-id',)

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_absolute_url(self):
        return ('organization_details', (), {'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Organization, self).save(*args, **kwargs)



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

    picture = models.ImageField(("Profile Picture"), upload_to="users/avatars/", null=True, blank=True)

    objects = ProfileManager()

    def __unicode__(self):
        return u"%s" % (self.user)

    def get_absolute_url(self):
        return ('profile_details', (), {})

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
    def organizations(self):
        return Organization.objects.filter(Q(people__in=[self,])|Q(admins__in=[self,]))

    @property
    def follows(obj):
        pass

