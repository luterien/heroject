from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from apps.actions.models import Invitation
from apps.actions.forms import InvitationForm
from apps.actions.utils import invite
from apps.projects.models import Project


class InviteToProject(CreateView):
    template_name = "invite_to_project.html"
    model = Invitation
    form_class = InvitationForm
    success_url = "/"

    def get_success_url(self):
        return reverse('project_details', kwargs={'pk': self.kwargs['project_id']})

    def form_valid(self, form):
        ## todo
        ## currently users are displayed in a select box,
        ## find a suitable widget later

        ## todo
        ## will be celery task
        invite(self.request.user, Project, self.kwargs['project_id'],
               form.instance.receiver)

        return redirect(self.get_success_url())



def invitations(request, template="profiles/invitations.html"):
    """
    invitation list for the user
    """

    ctx = {'profile': request.user}

    return render(request, template, ctx)

# TODO
# convert this to an ajax method


def reply_to_invitation(request, id,
                        template="profiles/reply_to_invitation.html"):
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

    return redirect('invitations')
