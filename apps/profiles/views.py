
from django.shortcuts import render
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType

from apps.profiles.models import *
from apps.profiles.forms import *
from apps.projects.forms import NewProjectForm
from apps.projects.models import Project



def index(request, template="index.html"):
    profile = Profile.objects.from_request(request)
    
    ctx = {'projects':profile.projects}

    return render(request, template, ctx)


def login_user(request,
               logged_in_url="/index/",
               login_success_url="/index/",
               template="login.html"):
    """
    login view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(logged_in_url)
    
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)
        form = AuthenticationForm(request.POST)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(login_success_url)
    else:
        form = AuthenticationForm()
    
    return render(request, template, {'form' : form }) 
            

def register_user(request,
                  register_success_url="/",
                  template="register.html",
                  logged_in_url="/"):
    """
    Registration view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(logged_in_url)
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # form is valid, register the user
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email']
            )
            user.save()

            auth_usr = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

            # create new profile
            prf = Profile(user=user)
            prf.save()

            if auth_usr:
                login(request, auth_usr)
            
            return HttpResponseRedirect(register_success_url)
    else:
        form = RegistrationForm()
    
    return render(request, template, {'form' : form })


@login_required
def logout_user(request, logout_success_url="/"):
    logout(request)
    return HttpResponseRedirect(logout_success_url)


@login_required
def profile_details(request, template="profiles/profile_details.html"):
    profile = Profile.objects.from_request(request)
    form = NewProjectForm()
    ctx = {'profile': profile,
          'form' : form }

    return render(request, template, ctx)


class OrganizationDetails(DetailView):
    template_name = "profiles/organization_details.html"
    model = Organization
    form_class = OrganizationForm


class CreateOrganization(CreateView):
    template_name = "profiles/create_organization.html"
    model = Organization
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse('organization_details',kwargs={'pk': self.object.id})

    def form_valid(self, form):
        # add the creater as an admin & regular user for this organization
        self.object = form.instance
        self.object.save()
        usr = Profile.objects.from_request(self.request)
        self.object.admins.add(usr)
        self.object.people.add(usr)
        return super(CreateOrganization, self).form_valid(form)


def invite(sender, cls, object_id, receiver=None, email=None):
    """
        if the receiver parameter is provided
        send an Invitation to the receiver

        otherwise send an email to the given address
    """
    if receiver:

        ## todo : action

        try:
            to = cls.objects.get(id=int(object_id))
            ivn = Invitation.objects.new(sender, to, receiver)
        except:
            to = None

    if email:
        pass
    

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




