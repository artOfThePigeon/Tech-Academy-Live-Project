from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.Form):
  Signature = forms.CharField(label='Signature', max_length=200, widget=forms.Textarea)
  Avatar = forms.ImageField(label='Avatar', help_text='max 42MB', required=False)

  class Meta:
    model = UserProfile
    fields = ('Signature', 'Avatar')

# Extends the base UserCreationForm
class SignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

  class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class ThreadCreateForm(ModelForm):
  ThreadTitle = forms.CharField(max_length=200, min_length=1, strip=True)
  ThreadBody = forms.CharField(
    max_length=1000,
    min_length=1,
    strip=True,
    widget=forms.Textarea,
  )


  class Meta:
    model = Thread
    fields = ('ThreadTitle', 'ThreadBody', 'Topic',)
'''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['Topic'].queryset = City.objects.none()
'''


class CommentCreateForm(ModelForm):
  CommentBody = forms.CharField(
    max_length=1000,
    min_length=1,
    strip=True,
    widget=forms.Textarea,
  )
  class Meta:
    model = Comment
    fields = ['CommentBody']

class FriendRequestForm(ModelForm):
  id = forms.ModelChoiceField(
    queryset = User.objects.all(),
  )
  class Meta:
    model = FriendConnection
    fields = ['id']
