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

  def get_queryset(self):
    return UserProfile.objects.order_by('-id')[::-1]

def user_profile_admin(request):
  pass

def get_profile(request):
  # if this is a post requestion we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request
    form = ProfileForm(request.POST)
    # check if valid
    if form.is_valid():
      # process the data in form as required
      # redirect to a new URL
      return HttpResponseRedirect('/submitted/')
    else:
      print(form.errors)

  else:
    form = ProfileForm()

  return render(request, 'user_profile/index.html', {'form': form})
