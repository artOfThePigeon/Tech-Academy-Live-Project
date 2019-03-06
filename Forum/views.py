from django.shortcuts import render_to_response, render
from django.views import generic
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .forms import ProfileForm
from .models import UserProfile
# Create your views here.

class UserProfileListView(generic.ListView):
  template_name = 'user_profile/index.html'
  context_object_name = 'users'


def get_profile(request):
  # if this is a post requestion we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request
    form = ProfileForm(request.POST or None, request.FILES or None)
    # check if valid
    if form.is_valid():
      # process the data in form as required
      # redirect to a new URL
      form = form.cleaned_data
      UserProfile.updateProfile(request, form)
      return HttpResponseRedirect('')
    else:
      print(form.errors)

  else:
    form = ProfileForm()
  context = {
    'form' : form,
  }

  return render(request, 'user_profile/index.html', context)
