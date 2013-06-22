from django.contrib.contenttypes.models import ContentType
from apps.actions.models import Action, Invitation, Notification, Follow


def action(user, action_object, action_key,
           target_object=None, send_notification=True):
    """ 
        create a new action and send a notification
    """
    action = Action.objects.new_action(user, action_object,
                                       action_key, target_object)

    if target_object and send_notification:
        notify_followers(action)


def invite(sender, cls, object_id, receiver=None, email=None):
    """
        if the receiver parameter is provided
        send an Invitation to the receiver

        otherwise send an email to the given address
    """
    if receiver:

        try:
            to = cls.objects.get(id=int(object_id))
            ivn = Invitation.objects.new(sender, to, receiver)
        except:
            to = None

        action(sender, receiver, "invite", target_object=to)
        
        # when an invitation is sent, notify the user
        # send_user_notification(action)

    if email:
        pass


def start_following(user, follow_object):
    """
        Start following the target_object
        Currently, it is only activated when a user is
        assigned to a task, or creates a discussion
    """
    flw = Follow.objects.create_new(user, follow_object)

    return flw


def notification_from_action(action, receiver):
    """
        Create a notification from the given action
    """
    
    n = Notification(sender=action.user,
                     receiver=receiver,
                     action_type=action.action_type,
                     action_content_type=action.action_content_type,
                     action_object_id=action.action_object_id,
                     target_content_type=action.target_content_type,
                     target_object_id=action.target_object_id)
    n.save()


def notify_followers(action, flws=None):
    """
        Create a notification from the given action,
        Send the message to everyone following the target_object of the action
    """

    # get followers for this object
    if not flws:
        flws = Follow.objects.filter(
            content_type=ContentType.objects.get_for_model(
                action.target_content_object.__class__),
            object_id=action.target_content_object.id)

    for flw in flws:
        notification_from_action(action, receiver=flw.follower)
