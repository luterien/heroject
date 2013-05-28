from django.contrib.contenttypes.models import ContentType

from apps.actions.models import Action, Invitation, Notification, Follow
from apps.profiles.models import Profile


def action(user, action_object, action_key, target_object=None, send_notification=True):
    """ 
        create a new action and send a notification
    """
    action = Action.objects.new_action(user, action_object, action_key, target_object)

    if target_object and send_notification:
        notification_from_action(action)


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

        action(sender.user, receiver, "invite", target_object=to)
        
        # when an invitation is sent, notify the user
        # send_user_notification(action)

    if email:
        pass


def start_following(user, follow_object):
    """
        Start following the target_object
        Currently, it is only activated when a user is assigned to a task, or creates a discussion
    """
    flw = Follow.objects.create_new(user, follow_object)

    return flw


def following(profile, limit=15):
    """
        Returns the items the user is following
    """
    flws = Follow.objects.filter(follower=profile.user)

    targets = [flw.content_object for flw in flws]

    # TODO : refactor

    ntfs = [n for n in Notification.objects.all() if n.target_content_object in targets]


    return ntfs[:limit]


def notification_from_action(action):
    """
        Create a notification from the given action
    """

    p = Profile.objects.get(user=action.user)
    
    n = Notification(sender = p,
                     action_type         = action.action_type,
                     action_content_type = action.action_content_type,
                     action_object_id    = action.action_object_id,
                     target_content_type = action.target_content_type,
                     target_object_id    = action.target_object_id)
    n.save()



