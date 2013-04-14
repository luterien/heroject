
from django.shortcuts import render_to_response, render
from django.contrib.auth import logout,login,authenticate
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from apps.profiles.models import *
from apps.utils import get_or_none
from apps.profiles.forms import *
from apps.projects.forms import NewProjectForm

def index(request, template="index.html"):
    profile = Profile.objects.from_request(request)
    
    ctx = {'projects':profile.projects}

    return render_to_response(template, ctx, context_instance=RequestContext(request))

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
    
    return render_to_response(template,
                              {'form' : form },
                              context_instance=RequestContext(request)) 
            

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
    
    return render_to_response(template,
                              {'form' : form },
                              context_instance=RequestContext(request)) 


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


@login_required
def organization_details(request, template=""):
    pass

