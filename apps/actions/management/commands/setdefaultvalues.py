from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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

        # the admin user has no Profile, create one
        admin = User.objects.filter(is_superuser=True)
        if admin.count() == 1:
            p, e = Profile.objects.get_or_create(user=admin[0])
            p.save()

            print "Profile created : %s" % e

            if e is True:
                print "Profile name : %s" % p

