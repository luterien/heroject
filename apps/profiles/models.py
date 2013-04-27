from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

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

    logo = models.ImageField(("Logo"), upload_to="/", null=True, blank=True)

    org_type = models.CharField(_("Organization Type"), max_length=60, choices=ORG_CHOICES, null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    people = models.ManyToManyField('Profile', verbose_name=_("People"), related_name="organization_list", null=True, blank=True)

    admins = models.ManyToManyField('Profile', verbose_name=_("Admins"), null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ('title',)

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

    picture = models.ImageField(("Profile Picture"), upload_to="/users/avatars/", null=True, blank=True)

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
        pass

    @property
    def invitations_sent(self):
        pass

    @property
    def organizations(self):
        return Organization.objects.filter(Q(people__in=[self,])|Q(admins__in=[self,]))



class InvitationManager(models.Manager):

    def active(self):
        """ 
            active/unread invitations
        """
        return self.filter(is_read=False)


    def new(self, sender, object, receiver=None):
        """
            create a new invitation
        """
        inv = self.model(sender=sender,
                         receiver=receiver,
                         content_type=ContentType.objects.get_for_model(object.__class__),
                         object_id=smart_unicode(object.id))
        inv.save()

        return inv


class Invitation(models.Model):
    """
        Store project, organization invitations
    """
    sender = models.ForeignKey(Profile, verbose_name="Sender")

    receiver = models.ForeignKey(Profile, verbose_name=_("Receiver"), null=True, blank=True, related_name="invitation_receiver")

    is_read = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)

    date_sent = models.DateTimeField(auto_now=True)

    objects = InvitationManager()

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        ordering = ('-date_sent',)

    def __unicode__(self):
        return "%s : %s -> %s" % (self.content_type, self.sender, self.receiver)

    def _type(self):
        pass

