from django.shortcuts import render_to_response, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import datetime
from .models import Comment, UserProfile, Topic, Thread

from .forms import ProfileForm, SignUpForm
from .models import UserProfile
# Create your views here.




# Account Views
@login_required
def home_view(request):
    #collect data for latest 10 threads on homepage
   data = Thread.objects.values().order_by('-DateUpdate')[:10]
   #convert to dictionary to pass variable
   threads = {"threads" : data}
   return render(request, 'index.html', threads)


class UserProfileListView(generic.ListView):
  template_name = 'user_profile/index.html'
  context_object_name = 'users'


def get_profile(request):
  # if this is a post request we need to process the form data
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
        form = SignUpForm(request.POST)
        if form.is_valid():
          user = form.save()
          user.refresh_from_db()
          UserProfile.objects.create(User_id=user.pk)
          raw_password = form.cleaned_data.get('password1')
          user = authenticate(username=user.username, password=raw_password)
          login(request, user)
          return redirect('home_view')
    else:
      form = SignUpForm()
    return render(request, 'Accounts/register.html', {'form': form})


# Forum views
class TopicsView(generic.ListView):
  model = Topic
  template_name = 'topics.html'


  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    context['threads'] = Thread.get_latest_thread
    print((context.get('threads')))
    return context

  def get_queryset(self):
    return Topic.objects.order_by('DateUpdated')

  def latest_topics(request, *args, **kwargs):
    my_context = Thread.get_latest_thread

    return render(request, 'topics.html', my_context)
