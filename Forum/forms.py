from django import forms
from .models import *

class ProfileForm(forms.Form):
  Signature = forms.CharField(label='Signature', max_length=200)
  Avatar = forms.ImageField(label='Avatar')
  class Meta:
    model = UserProfile
    fields = ('Signature', 'Avatar')
