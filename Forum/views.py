from django.shortcuts import render_to_response, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from itertools import chain, groupby
from django.db import connection
from collections import namedtuple
import datetime
from .models import Comment, UserProfile, Topic, Thread, Message, FriendConnection
from django.db.models import Q
from functools import reduce

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

# Messaging
def message(request):
    
    user = request.user

    if request.method == 'POST':

        # Defining where text will come from on template
        content = request.POST['content']
        reciever = request.POST['reciever']

        
        reciever_used = User.objects.get(username=reciever)# Gets the username of the receiver from the db
        sender_used = user # Sender is current user

        message = Message() # Creating connection to the db
        # Setting respective table fields to template content
        message.MessageBody = content 
        message.ReceivingUser = reciever_used
        message.SendingUser = sender_used
        message.save() # Saving to the db

        # Return information to send message
        return render(request, 'Message/message.html', {'message': message} )

    else:

        # Query the FriendConnection table to get the ids of current users friends
        friend_list = FriendConnection.objects.filter((Q(ReceivingUser=user) | Q(SendingUser=user))& Q(IsConfirmed=True)) 
        # Create a list of friends user ids
        friend_ids = list(friend_list.values('ReceivingUser_id'))
        receiver_id_list = [] # Empty list for the ids

        # Iterate through the list, appending the user ids
        for id in friend_ids:
            receiver_id_list.append(id['ReceivingUser_id'])
            
        receiver_name_list = [] # Empty list for the receiver username

        # Iterate through the id list, grabbing the username and appending it to the new empty list
        for id in receiver_id_list:
            user = User.objects.get(id=id)
            username = user.username
            receiver_name_list.append(username)

        # Context variable to hold the list of the friend usernames
        context = {
            'receiver_choices': receiver_name_list,
        }

        # Return list of friends usernames
        return render(request,'Message/message.html', context)

# Main Inbox
def inbox(request):

    # Populate all messages to current user.
    if request.user.is_authenticated:
        currentUser = request.user.id
        messages = Message.objects.filter(ReceivingUser_id=currentUser).order_by('-DateSent')
        
        # Return messages to be placed in template
        return render(request, 'Message/inbox.html', {'messages': messages})
    
    else:
        return render(request, 'Message/inbox.html', {})

# Message Details (Shows all messages from selected sender)
def messagedetails(request):

    
    currentUser = request.user.id # Set current user
    message_id = request.GET.get('message_id') # Get the id of the selected message from Main Inbox 
    message = Message.objects.get(id=message_id) # Get the message entry from the db
    sendingUser = message.SendingUser.id # Get the sending user id from the db
    
    # Query the db for all messages from selected sender and order decending
    messages = Message.objects.filter(ReceivingUser_id=currentUser, SendingUser_id=sendingUser).order_by('-DateSent')
    
    # Return the list of messages to the template to be placed
    return render(request, 'Message/messagedetails.html', {'messages': messages})
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
