from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView

from apps.actions.forms import *
from apps.profiles.models import *
from apps.profiles.forms import *
from apps.projects.forms import NewProjectForm
from apps.profiles.decorators import anonymous_required


@login_required
def index(request, template="index.html"):
    
    ctx = {'projects': request.user.projects}

    return render(request, template, ctx)

@anonymous_required('index')
def login_user(request,
               login_success_url="/index/",
               template="login.html"):
    """
    Login view
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        form = LoginForm(request.POST)
        if user is not None:
            login(request, user)
            return redirect(login_success_url)
    else:
        form = LoginForm()
    
    return render(request, template, {'form': form})
            
@anonymous_required('index')
def register_user(request,
                  register_success_url="/",
                  template="register.html"):
    """
    Registration view
    """
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user = Profile.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'])

            user.save()

            auth_usr = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])

            if auth_usr:
                login(request, auth_usr)
            
            return redirect(register_success_url)
    else:
        form = RegistrationForm()
    
    return render(request, template, {'form': form})


@login_required
def logout_user(request, logout_success_url="/"):
    logout(request)
    return redirect(logout_success_url)


@login_required
def profile_details(request, template="profiles/profile_details.html"):
    form = NewProjectForm()
    ctx = {'profile': request.user,
           'form': form}

    return render(request, template, ctx)


class OrganizationDetails(DetailView):
    template_name = "profiles/organization_details.html"
    model = Organization
    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        invitation_form = InvitationForm()
        invitation_form.fields['receiver'].queryset = Profile.objects.exclude(
            id__in=self.object.people.values_list('id', flat=True))
        return super(OrganizationDetails, self).get_context_data(
            **{'invitation_form': invitation_form})


class CreateOrganization(CreateView):
    template_name = "profiles/create_organization.html"
    model = Organization
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse('organization_details',
                       kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        # add the creater as an admin & regular user for this organization
        self.object = form.instance
        self.object.save()
        self.object.admins.add(self.request.user)
        self.object.people.add(self.request.user)
        return super(CreateOrganization, self).form_valid(form)


class OrganizationUpdate(UpdateView):
    template_name = "update_organization.html"
    model = Organization
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse('update_organization',
                       kwargs={'slug': self.object.slug})

    #def form_valid(self, form):
    #    pass


class ProfileUpdate(UpdateView):
    template_name = "update_profile.html"
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return request.user

    def get_initial(self):
        """ get the initial value for user.email """
        init = super(ProfileUpdate, self).get_initial()
        init.update({'email': self.request.user.email})
        return init

    def get_success_url(self):
        return reverse('update_profile')

    def form_valid(self, form):
        # update the email on user model
        self.object = form.instance

        email = form.cleaned_data.get('email')

        self.object.email = email
        self.object.save()

        return super(ProfileUpdate, self).form_valid(form)


def notifications(request, template="notifications.html"):
    """
        Display the list of notifications for the user
    """
    from apps.actions.models import Notification

    ntfs = Notification.objects.filter(receiver=request.user)
    
    ctx = {'notifications': ntfs}

    return render(request, template, ctx)
