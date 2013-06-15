from django.core.management.base import BaseCommand
from apps.profiles.models import Profile
from apps.actions.models import ActionType


class Command(BaseCommand):
    help = "Create the default values for project to function properly"

    def handle(self, *args, **options):
        
        # create the basic ActionTypes
        action_type_lst = [
            ('create',  'created',   '',   '%(user)s has created %(action_object)s'),
            ('delete',  'deleted',   '',   '%(user)s has deleted %(action_object)s'),
            ('comment', 'commented', 'on', '%(user)s has commented on %(target_object)s'),
            ('invite',  'invited',   'to', '%(user)s has invited %(action_object)s to %(target_object)s'),
            ('assign',  'assigned',  'to', '%(user)s has assigned %(action_object)s to %(target_object)s')
        ]

        for tpl in action_type_lst:
            name, verb, prep, format = tpl
            at, ex = ActionType.objects.get_or_create(name=name,
                                                      verb=verb,
                                                      preposition=prep,
                                                      format=format)
            at.save()

            print "ActionType created : %s" % ex

            if ex is True:
                print "ActionType added : %s" % at


