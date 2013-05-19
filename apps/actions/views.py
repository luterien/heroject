from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from apps.actions.models import Invitation
from apps.actions.forms import InvitationForm
from apps.profiles.models import Profile, Organization
from apps.actions.utils import invite
from apps.projects.models import Project

class InviteToProject(CreateView):
    template_name = "invite_to_project.html"
    model = Invitation
    form_class = InvitationForm
    success_url = "/"

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):

        ## todo
        ## currently users are displayed in a select box, find a suitable widget later

        sender = Profile.objects.from_request(self.request)

        invite(sender, Project, self.kwargs['project_id'], form.instance.receiver)

        return HttpResponseRedirect(self.get_success_url())


class InviteToOrganization(CreateView):
    template_name = "invite_to_organization.html"
    model = Invitation
    form_class = InvitationForm
    success_url = "/"

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):

        ## todo
        ## basic controls

        sender = Profile.objects.from_request(self.request)

        invite(sender, Organization, self.kwargs['organization_id'], form.instance.receiver)

        return HttpResponseRedirect(self.get_success_url())


def invitations(request, template="profiles/invitations.html"):
    """
        invitation list for the user
    """
    p = Profile.objects.from_request(request)

    ctx = {'profile':p}

    return render(request, template, ctx)

# TODO
# convert this to an ajax method

def reply_to_invitation(request, id, template="profiles/reply_to_invitation.html"):
    """
        accept or refuse an invitation
    """
    invitation = Invitation.objects.get(id=id)

    is_accepted = request.GET.get('is_accepted', False)

    if is_accepted:
        invitation.is_accepted = True
        # TODO : fix this part later
        invitation.add_user()

    invitation.is_read = True
    invitation.save()

    return HttpResponseRedirect(reverse('invitations'))
