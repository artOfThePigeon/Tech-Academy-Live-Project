from django.shortcuts import render_to_response, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from itertools import chain, groupby
from django.db import connection
from collections import namedtuple
import datetime
from .models import Comment, UserProfile, Topic, Thread

from .forms import ProfileForm, SignUpForm
from .models import UserProfile
# Create your views here.


# Helper Fucntions
def dictfetchall(query):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
      cursor.execute(query)
      columns = [col[0] for col in cursor.description]
      for col in columns:
        print(col)
      return [
          dict(zip(columns, row))
          for row in cursor.fetchall()
    ]



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

  def get_queryset(self):
    return dictfetchall('''SELECT Forum_thread.id as thread_id,
                            Forum_topic.TopicTitle as "topic_title",
                            ThreadTitle as thread_title,
                            Forum_topic.ThreadCount as thread_count,
                            MAX(Forum_thread.DateUpdate) as update_date
                            FROM Forum_thread
                            INNER JOIN Forum_topic
                            ON Forum_topic.id = Forum_thread.Topic_id
                            GROUP BY Topic_id
                            ORDER BY Forum_topic.id ASC''')
