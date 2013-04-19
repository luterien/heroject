from django.db import models
from django.contrib.auth.models import User
from apps.profiles.models import Profile
from projectbonus.utils import slugify


# NOTE
# Still under construction


ADDITION = "Addition"
CHANGE = "Change"
DELETE = "Delete"
CHECK = "Check"
UNCHECK = "Uncheck"


ACTION_TYPES = (
    ('add', ADDITION),
    ('change', CHANGE),
    ('delete', DELETE),
    ('check', CHECK),
    ('uncheck', UNCHECK),
)

MSG_DICT = {
    
}


class Action(models.Model):
    action_time = models.DateTimeField(_("action time"), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_("user"), blank=True, null=True, on_delete=models.SET_NULL)

    ip_address = models.CharField(_("IP address"), blank=True, null=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)
    content_object = models.GenericForeignKey('content_type', 'object_id')

    action_type = models.CharField(_('action type'), choices=ACTION_TYPES)

    def __unicode__(self):
        pass


class Notification(models.Model):
    title = models.CharField(_("Title"), max_length=60)
    message = models.CharField(_("Message"), max_length=300)

    action_time = models.DateTimeField(_("Action time"), auto_now=True)

    receiver = models.ForeignKey(Profile, verbose_name="Receiver")
    sender = models.ForeignKey(Profile, verbose_name="Sender", null=True, blank=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ('-action_time',)

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