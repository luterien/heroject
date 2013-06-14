import re
from django import forms
from django.contrib.auth.models import User
from apps.profiles.models import Organization, Profile
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    username = forms.CharField(label=u"Username", max_length=30)
    email = forms.EmailField(label=u"E-Mail")
    password1 = forms.CharField(label=u"Password",
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=u"Password (Again)",
                                widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"placeholder": "Username"}
        self.fields["email"].widget.attrs = {"placeholder": "E-Mail"}
        self.fields["password1"].widget.attrs = {"placeholder": "Password"}
        self.fields["password2"].widget.attrs = {"placeholder": "Password (Again)"}
    
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
                                        'alphanumeric characters and'
                                        ' the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        raise forms.ValidationError('Username is already taken.')


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('title', 'description', 'logo', )


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(label="E-Mail")

    class Meta:
        model = Profile
        fields = ('picture', )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"placeholder": "Username"}
        self.fields["password"].widget.attrs = {"placeholder": "Password"}
        

