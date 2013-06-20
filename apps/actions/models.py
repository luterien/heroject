from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.conf import settings

from apps.projects.models import Project


class ActionType(models.Model):
    """
        examples of usage : 

        -> add <this> to <that>
        -> invite <this> to <that>
        -> remove <this> from <that>
        -> assign <this> to <that>
        -> comment on <that>
    """
    name = models.CharField(_('Action name/key'), max_length=30)
    verb = models.CharField(_('Verb'), max_length=40)
    
    preposition = models.CharField(_('Preposition'), max_length=20,
                                   null=True, blank=True)
    
    format = models.CharField(_('Format'), max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name
    
    def validate_format(self):
        pass
    
    def get_format(self):
        return self.format
    
    def format_dict(self):
        return {'verb': self.verb, 'prep': self.preposition}


class ActionManager(models.Manager):

    def new_action(self, user, action_object, action_key, target_object=None):
        """
            Create an action

            If the target_object is on the user's follow list
            Send the user a notification
        """
        action_types = ActionType.objects.filter(name=action_key)
        if not action_types.exists():
            action_types.create(name=action_key)

        action = self.model(
            user=user,
            action_content_type=ContentType.objects.get_for_model(
                action_object.__class__),
            action_object_id=smart_unicode(action_object.id),
            action_type=action_types.get())

        if target_object:
            action.target_content_type = ContentType.objects.get_for_model(
                target_object.__class__)
            action.target_object_id = smart_unicode(target_object.id)

        action.save()
        return action


class Action(models.Model):
    """

        User action examples :
    
        -> <ahmet> has <deleted> <discussionTitle>
        -> <ercan> has <commented> <on> <taskTitle>
        -> <erhan> has <created> <projectTitle>
        -> <murat> has <assigned> <userName> to <taskName>
        -> <ayhan> has <changed> <taskTitle>

    """
    action_time = models.DateTimeField(_("action time"), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), blank=True,
                             null=True, on_delete=models.SET_NULL)

    ## TODO : remove this field
    ip_address = models.CharField(_("IP address"), max_length=20,
                                  blank=True, null=True)

    action_content_type = models.ForeignKey(
        ContentType, related_name="action_object", blank=True, null=True)
    action_object_id = models.TextField(_('object id'), blank=True, null=True)

    action_content_object = generic.GenericForeignKey(
        'action_content_type', 'action_object_id')

    action_type = models.ForeignKey(ActionType, verbose_name=_('action type'))

    target_content_type = models.ForeignKey(
        ContentType, related_name="target_object", blank=True, null=True)

    target_object_id = models.TextField(_('object id'), blank=True, null=True)

    target_content_object = generic.GenericForeignKey('target_content_type',
                                                      'target_object_id')

    objects = ActionManager()

    class Meta:
        verbose_name = _("User Action")
        verbose_name_plural = _("User Actions")
        #ordering = ('-action_time')

    def __unicode__(self):
        return self.formatted or "xx"

    def _construct_action_message(self):
        """
            Construct an action message
        """
        prep = self.action_type.preposition
        target_obj = self.target_content_object

        if prep and target_obj:
            msg = "%s has %s %s %s %s" % (self.user, self.action_type.verb,
                                          self.action_content_object, prep,
                                          target_obj)
        else:
            msg = "%s has %s %s %s" % (self.user, self.action_type.verb,
                                       prep, self.action_content_object)

        return _(msg.strip())
    
    @property
    def default_format(self):
        if self.target_content_object and self.action_type and self.action_type.preposition:
            return "%(user)s has %(verb)s %(action_object)s %(prep)s %(target_object)s"
        return "%(user)s has %(verb)s %(prep)s %(action_object)s"
    
    def get_format(self):
        if self.action_type and self.action_type.format:
            return self.action_type.format or "dd"
        else:
            return self.default_format
    
    @property
    def formatted(self):
        format = self.get_format()
        
        formatted = format % self.format_dict
        
        return formatted

    @property
    def format_dict(self):
        keys = self.action_type.format_dict()
        
        dx = {
              'action_object': self.action_content_object,
              'target_object': self.target_content_object,
              'user': self.user,
              'date': self.action_time
        }
        
        keys.update(dx)
        
        return keys


class FollowManager(models.Manager):

    def create_new(self, user, flw_object):
        """
            
        """
        flw = self.model(
            follower=user,
            content_type=ContentType.objects.get_for_model(
                flw_object.__class__),
            object_id=smart_unicode(flw_object.id))

        flw.save()

        return flw


class Follow(models.Model):
    """
        Lets a user follow an object (Project, Task etc)
    """
    follower = models.ForeignKey(settings.AUTH_USER_MODEL)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    is_active = models.BooleanField(default=True)

    objects = FollowManager()

    def __unicode__(self):
        return u"%s following %s" % (self.follower, self.content_object)


class Notification(models.Model):
    """
        Store notification data
    """
    notice_time = models.DateTimeField(_("action time"), auto_now=True)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), blank=True,
                               null=True, on_delete=models.SET_NULL)

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"),
                                 blank=True, null=True,
                                 related_name="received_notifications",
                                 on_delete=models.SET_NULL)

    action_type = models.ForeignKey(ActionType, verbose_name=_('action type'))

    action_content_type = models.ForeignKey(
        ContentType, related_name="notice_action_object",
        blank=True, null=True)

    action_object_id = models.TextField(_('object id'), blank=True, null=True)

    action_content_object = generic.GenericForeignKey('action_content_type',
                                                      'action_object_id')

    target_content_type = models.ForeignKey(
        ContentType, related_name="notica_target_object",
        blank=True, null=True)

    target_object_id = models.TextField(_('object id'), blank=True, null=True)
    target_content_object = generic.GenericForeignKey('target_content_type',
                                                      'target_object_id')

    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        #ordering = ('-notice_time',)

    def __unicode__(self):
        return self._construct_notification_message()

    def _construct_notification_message(self):
        """
            Construct an action message
        """
        prep = self.action_type.preposition
        target_obj = self.target_content_object

        if prep and target_obj:
            msg = "%s has %s %s %s %s" % (self.sender, self.action_type.verb,
                                          self.action_content_object, prep,
                                          target_obj)
        else:
            msg = "%s has %s %s %s" % (self.sender, self.action_type.verb,
                                       prep, self.action_content_object)

        return _(msg.strip())


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
                         content_type=ContentType.objects.get_for_model(
                             object.__class__),
                         object_id=smart_unicode(object.id))
        inv.save()

        return inv


class Invitation(models.Model):
    """
        Store project invitations
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Sender")

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"),
                                 null=True, blank=True,
                                 related_name="received_invitations")

    is_read = models.BooleanField(default=False)

    is_accepted = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)

    object_id = models.TextField(_('object id'), blank=True, null=True)

    content_object = generic.GenericForeignKey('content_type', 'object_id')

    date_sent = models.DateTimeField(auto_now=True)

    objects = InvitationManager()

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        ordering = ('-date_sent',)

    def __unicode__(self):
        return "%s : %s -> %s" % (self.content_type,
                                  self.sender, self.receiver)

    def message(self):
        return "%s has invited you to %s" % (self.sender,
                                             self.content_object)

    def add_user(self):
        # TODO : find a better solution for this part
        if isinstance(self.content_object, Project):
            self.content_object.people.add(self.receiver)
            self.content_object.save()


