from django import forms
from django.utils.translation import ugettext as _

from apps.actions.models import Invitation


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ('receiver',)


class InvitationWithMailForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))

