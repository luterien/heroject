from django.core.management.base import BaseCommand
from apps.profiles.models import Profile
from apps.actions.models import ActionType


class Command(BaseCommand):
    help = "Create the default values for project to function properly"

    def handle(self, *args, **options):
        
        # create the basic ActionTypes
        action_type_lst = [
            ('create', 'created', ''),
            ('delete', 'deleted', ''),
            ('comment', 'commented', 'on'),
            ('invite', 'invited', 'to'),
            ('assign', 'assigned', 'to')
        ]

        for tpl in action_type_lst:
            name, verb, prep = tpl
            at, ex = ActionType.objects.get_or_create(name=name,
                                                      verb=verb,
                                                      preposition=prep)
            at.save()

            print "ActionType created : %s" % ex

            if ex is True:
                print "ActionType added : %s" % at


