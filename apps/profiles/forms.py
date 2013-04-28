
import re

from django import forms
from django.contrib.auth.models import User

from apps.profiles.models import Invitation, Organization, Profile


class RegistrationForm(forms.Form):
    username = forms.CharField(label=u"Username", max_length=30)
    email = forms.EmailField(label=u"E-Mail")
    password1 = forms.CharField(label=u"Password",widget=forms.PasswordInput())
    password2 = forms.CharField(label=u"Password (Again)",widget=forms.PasswordInput())
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain '
            'alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        raise forms.ValidationError('Username is already taken.')



class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ('receiver',)


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('title', 'description', 'logo', )


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(label="E-Mail")

    class Meta:
        model = Profile
        fields = ('picture', )
