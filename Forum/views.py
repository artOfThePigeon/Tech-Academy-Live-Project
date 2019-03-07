from django.shortcuts import render_to_response, render
from django.views import generic
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
import datetime

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


def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_joined = datetime.datetime.now()
        u1 = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, date_joined=date_joined)
        u1.save()

        #return redirect('') Can redirect to a site here when one is available.
        return render(request, 'Accounts/register.html')
    else:
        return render(request, 'Accounts/register.html')
