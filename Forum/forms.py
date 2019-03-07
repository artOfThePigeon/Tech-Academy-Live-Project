from django import forms
from .models import *

class ProfileForm(forms.Form):
  Signature = forms.CharField(label='Signature', max_length=200)
  Avatar = forms.ImageField(label='Avatar', help_text='max 42MB', required=False)
  class Meta:
    model = UserProfile
    fields = ('Signature', 'Avatar')
