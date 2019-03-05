from django import forms
from .models import *

class ProfileForm(forms.Form):
  sig = forms.CharField(label='Signature', max_length=200)
  avatar = forms.ImageField(label='Avatar')
  class Meta:
    model = UserProfile
    fields = ('Signature', 'Avatar')
