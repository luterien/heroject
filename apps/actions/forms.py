from django import forms
from apps.actions.models import Invitation


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ('receiver',)

