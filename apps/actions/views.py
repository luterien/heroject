from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.models import get_current_site
from django.contrib import messages
from django.utils.translation import ugettext as _

from apps.actions.models import Invitation
from apps.actions.forms import InvitationForm, InvitationWithMailForm
from apps.actions.tasks import invite
from apps.projects.models import Project
from apps.profiles.tasks import mail_sender
from django.contrib import messages

from heroject.settings import EMAIL_HOST_USER


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

        invite.delay(self.request.user, Project, self.kwargs['project_id'],
               form.instance.receiver)
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Your invitation has successfully sended to recepient."))

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


def invite_with_mail(request, template='mail/invite_with_mail.html'):
    if request.method == 'POST':
        form = InvitationWithMailForm(request.POST)
        if form.is_valid():
            inviter = request.user
            current_site = get_current_site(request)

            #TODO: Erhan we need a mail template to send users to invite
            subject = "%s Has Invited You to Heroject" % inviter.username
            message = render_to_string('mail/invitation_mail.html',
                                       {'site': current_site.domain,
                                        'full_name': inviter.get_full_name()})

            sender = EMAIL_HOST_USER
            recipients = [form.cleaned_data['email']]

            mail_sender.delay(subject=subject, message=message,
                              sender=sender, recipients=recipients)
            messages.add_message(
                request, messages.SUCCESS,
                _("Your invitation has successfully sended to recepient."))

            form = InvitationWithMailForm()

            redirect('invite_with_mail')
    else:
        form = InvitationWithMailForm()

    return render(request, template, {'form': form})

