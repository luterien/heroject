from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager

from projectbonus.utils import slugify
from apps.profiles.tasks import make_square

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

    logo = models.ImageField(_('Logo'), upload_to="organizations/logos/",
                             null=True, blank=True)

    org_type = models.CharField(_("Organization Type"), max_length=60,
                                choices=ORG_CHOICES, null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    people = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("People"),
                                    related_name="organization_list",
                                    null=True, blank=True)

    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Admins"),
                                    null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ('-id',)

    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('organization_details', (), {'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, instance=self)
        super(Organization, self).save(*args, **kwargs)
        if self.logo:
            make_square(self.logo.path)


class ProfileManager(UserManager):

    def from_request(self, request, *args, **kwargs):
        return request.user


class Profile(AbstractUser):

    birthdate = models.DateTimeField(_("Birth Date"),
                                     null=True, blank=True)

    picture = models.ImageField(_("Profile Picture"),
                                upload_to="users/avatars/",
                                null=True, blank=True)

    objects = ProfileManager()

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
    def organizations(self):
        return Organization.objects.filter(
            Q(people__in=[self, ]) | Q(admins__in=[self, ]))

    @property
    def follows(self, obj):
        pass




