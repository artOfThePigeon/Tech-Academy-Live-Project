from django.shortcuts import render_to_response, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime
from .models import Comment, UserProfile, Topic, Thread, Message, FriendConnection
from django.db.models import Q
from functools import reduce

from .forms import ProfileForm
from .models import UserProfile
# Create your views here.

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

        return redirect('home_view')
    else:
        return render(request, 'Accounts/register.html')

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