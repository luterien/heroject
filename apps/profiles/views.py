from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.template.loader import render_to_string

from apps.profiles.models import *
from apps.profiles.forms import *
from apps.projects.forms import NewProjectForm
from apps.profiles.decorators import anonymous_required
from apps.profiles.tasks import mail_sender

from heroject.settings import EMAIL_HOST_USER


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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = Profile.objects.create_user(
                username=username,
                email=email,
                password=password)

            user.save()

            #TODO: Erhan we need a mail template to send users to say hello
            subject = "Welcome to Heroject"
            message = render_to_string('mail/welcome_mail.html',
                                       {'username': username,
                                        'password': password,
                                        'email': email})

            sender = EMAIL_HOST_USER
            recipients = [email]

            mail_sender.delay(subject=subject, message=message,
                              sender=sender, recipients=recipients)

            auth_usr = authenticate(username=username,
                                    password=password)

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


class ProfileUpdate(UpdateView):
    template_name = "update_profile.html"
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

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
