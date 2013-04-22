from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from apps.profiles.models import Profile
from projectbonus.utils import slugify


class ActionType(models.Model):
    """
        todo : refactor
    """
    name = models.CharField(_('Action name'), max_length=30)
    verb = models.CharField(_('Verb'), max_length=40)

    preposition = models.CharField(_('Preposition'), max_length=20, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % (self.name)


class ActionManager(models.Manager):

    def new_action(self, user, actor_object, action_type, target_object=None):
        """
            Create an action
        """
        action = self.model(user=user,
                            actor_content_type=ContentType.objects.get_for_model(actor_object.__class__),
                            actor_object_id=smart_unicode(actor_object.id),
                            action_type=action_type)

        if target_object:
            action.target_content_type = ContentType.objects.get_for_model(target_object.__class__),
            action.target_object_id = smart_unicode(target_object.id)

        action.save()


class Action(models.Model):
    """

        User action examples :
    
        -> <ahmet> has <deleted> <discussionTitle>
        -> <ercan> has <commented on> <taskTitle>
        -> <erhan> has <created> <projectTitle>
        -> <murat> has <assigned> <userName> to <taskName>
        -> <ayhan> has <changed> <taskTitle>

    """
    action_time = models.DateTimeField(_("action time"), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_("user"), blank=True, null=True, on_delete=models.SET_NULL)

    ip_address = models.CharField(_("IP address"), max_length=20, blank=True, null=True)

    actor_content_type = models.ForeignKey(ContentType, related_name="actor_object", blank=True, null=True)
    actor_object_id = models.TextField(_('object id'), blank=True, null=True)
    actor_content_object = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    action_type = models.ForeignKey(ActionType, verbose_name=_('action type'))

    target_content_type = models.ForeignKey(ContentType, related_name="target_object", blank=True, null=True)
    target_object_id = models.TextField(_('object id'), blank=True, null=True)
    target_content_object = generic.GenericForeignKey('target_content_type', 'target_object_id')

    objects = ActionManager()

    class Meta:
        verbose_name = _("User Action")
        verbose_name_plural = _("User Actions")
        #ordering = ('-action_time')

    def __unicode__(self):
        return self._construct_action_message()

    def _construct_action_message(self):
        """
            Construct an action message
        """
        prep = self.action_type.preposition
        target_obj = self.target_content_object

        if prep and target_obj:
            msg = "%s has %s %s %s %s" % (self.user, self.action_type.verb, self.actor_content_object, prep, target_obj)
        else:
            msg = "%s has %s %s" % (self.user, self.action_type.verb, self.actor_content_object)

        return _(msg)


class Notification(models.Model):
    title = models.CharField(_("Title"), max_length=60)
    message = models.CharField(_("Message"), max_length=300)

    action_time = models.DateTimeField(_("Action time"), auto_now=True)

    receiver = models.ForeignKey(Profile, verbose_name="Receiver", related_name="receiver_object")
    sender = models.ForeignKey(Profile, verbose_name="Sender", null=True, blank=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        #ordering = ('-action_time',)

    def __unicode__(self):
        pass

    def _construct_notification_message(action):
        pass


def send_notification(type, subject, receiver, sender=None):

    title = "" # generate title
    message = "" # generate message

    notification = Notification(title = title,
                                message = message,
                                receiver = receiver)
    if sender:
        notification.sender = sender

    notification.save()


def get_ip_address(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
        # in case of multiple IP's
        ip_addr = ip.split(',')[0]
    except:
        ip_addr = None

    return ip_addr