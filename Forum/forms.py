from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
  Signature = forms.CharField(label='Signature', max_length=200)
  class Meta:
    model = UserProfile
    fields = ('Signature', 'Avatar')
