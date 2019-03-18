from django.shortcuts import render_to_response, render, redirect, reverse
from django.views import generic
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from itertools import chain, groupby
from django.db import connection
from collections import namedtuple
import datetime
from .models import Comment, UserProfile, Topic, Thread, Message, FriendConnection
from django.db.models import Q
from functools import reduce
from django.views.generic.edit import FormView, CreateView
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .forms import ProfileForm, SignUpForm, CommentCreateForm, ThreadCreateForm, FriendRequestForm
from .models import UserProfile, FriendConnection, Upvote
# Create your views here.


# Helper Fucntions

# This makes a dictionary out of a custom SQL query
def dictfetchall(query):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]



# Account Views
@login_required
def home_view(request):
    # collect data for latest 10 threads on homepage
    data = Thread.objects.values().order_by('-DateUpdate')[:10]
    # convert to dictionary to pass variable
    threads = {"threads": data}
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
            return HttpResponseRedirect('/')
        else:
            print(form.errors)

    else:
      sig = request.user.userprofile.Signature
      form = ProfileForm({'Signature': sig})
    context = {
      'form': form,
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



# Return a dictionary of thread topics
class TopicsView(generic.ListView):
    model = Topic
    template_name = 'topics.html'

    def get_queryset(self):
        return dictfetchall('''SELECT Forum_thread.id as thread_id,
                            Forum_topic.TopicTitle as "topic_title",
                            ThreadTitle as thread_title,
                            COUNT(Forum_thread.id) as thread_count,
                            MAX(Forum_thread.DateUpdate) as update_date
                            FROM Forum_thread
                            INNER JOIN Forum_topic
                            ON Forum_topic.id = Forum_thread.Topic_id
                            GROUP BY Topic_id
                            ORDER BY Forum_topic.id ASC''')



class ThreadCreateView(CreateView):
  template_name = 'forum/thread_form.html'
  model = Thread
  form_class = ThreadCreateForm

  def form_valid(self, form):
    form = form.save(commit=False)
    form.Author = self.request.user
    form.ViewCount = 1
    form.PostCount = 0
    today = datetime.date.today().strftime('%Y-%m-%d')
    form.DateStarted = today
    form.DateUpdate = today
    form.save()
    return HttpResponseRedirect("/home/thread/{}/".format(form.id))



@login_required
@require_http_methods(['POST'])
def create_comment(request, slug):
  if request.method == 'POST':
      form = CommentCreateForm(request.POST)
      if form.is_valid():
          form = form.save(commit=False)
          thread = Thread.objects.get(id=slug)
          form.User = request.user
          form.Thread = thread
          thread.DateUpdate = datetime.date.today().strftime('%Y-%m-%d')
          count = Comment.objects.filter(Thread_id=slug).count()
          # count + 1 because it won't count the post we are about to make
          thread.PostCount = count + 1
          form.save()
          thread.save()
          return HttpResponseRedirect("/home/thread/{}/".format(slug))
  else:
    return HttpResponseBadRequest()



def upvote_thread(request, *args, **kwargs):
  if request.user.is_authenticated:
    if request.method == 'GET':
      userID = request.user.id
      threadID = kwargs['id']
      user_upvoted_thread = Upvote.objects.filter(Thread_id=threadID, User_id=userID)
      if user_upvoted_thread.count():
        user_upvoted_thread.delete()
      else:
        Upvote.objects.create(Thread_id=threadID, User_id=userID)

      thread = Thread.objects.get(id=threadID)
      count = Upvote.objects.filter(Thread_id=threadID).count()
      thread.UpVoteCount = count
      thread.save()
      return HttpResponse(count)
  else:
    HttpResponseRedirect("{% url 'login' %}")




# Display the comments of a thread
class CommentThread(generic.ListView):
    template_name = 'forum/comment_thread.html'
    context_object_name = 'comments'
    paginated_by = 10
    ordering = ['-DateCreated']


    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        return Comment.objects.filter(Thread_id=pk).order_by('DateCreated').reverse


    def get_context_data(self, *args, **kwargs):
        context = super(CommentThread, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['thread'] = Thread.objects.filter(id = pk).last
        context['form'] = CommentCreateForm()

        return context



# Messaging
def message(request):

    user = request.user

    if request.method == 'POST':

        # Defining where text will come from on template
        content = request.POST['content']
        reciever = request.POST['reciever']
        # Add subject line to message
        subject = request.POST['subject']

        # Gets the username of the receiver from the db
        reciever_used = User.objects.get(username=reciever)
        sender_used = user  # Sender is current user

        message = Message()  # Creating connection to the db
        # Setting respective table fields to template content
        message.MessageBody = content
        message.Subject = subject
        message.ReceivingUser = reciever_used
        message.SendingUser = sender_used
        message.save()  # Saving to the db

        # Return information to send message
        return render(request, 'Message/message.html', {'message': message})

    else:

        # Query the FriendConnection table to get the ids of current users friends
        friend_list = FriendConnection.objects.filter(
            (Q(ReceivingUser=user) | Q(SendingUser=user)) & Q(IsConfirmed=True))
        # Create a list of friends user ids
        friend_ids = list(friend_list.values('ReceivingUser_id'))
        receiver_id_list = []  # Empty list for the ids

        # Iterate through the list, appending the user ids
        for id in friend_ids:
            receiver_id_list.append(id['ReceivingUser_id'])

        receiver_name_list = []  # Empty list for the receiver username

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
        return render(request, 'Message/message.html', context)



# Main Inbox
def inbox(request):

    # Populate all messages to current user.
    if request.user.is_authenticated:
        currentUser = request.user.id
        messages = Message.objects.filter(
            ReceivingUser_id=currentUser).order_by('-DateSent')

        # Return messages to be placed in template
        return render(request, 'Message/inbox.html', {'messages': messages})

    else:
        return render(request, 'Message/inbox.html', {})




# Message Details (Shows all messages from selected sender)
def messagedetails(request):

    currentUser = request.user.id  # Set current user
    # Get the id of the selected message from Main Inbox
    message_id = request.GET.get('message_id')
    # Get the message entry from the db
    message = Message.objects.get(id=message_id)
    sendingUser = message.SendingUser.id  # Get the sending user id from the db

    # Query the db for all messages from selected sender and order decending
    messages = Message.objects.filter(
        ReceivingUser_id=currentUser, SendingUser_id=sendingUser).order_by('-DateSent')

    # Return the list of messages to the template to be placed
    return render(request, 'Message/messagedetails.html', {'messages': messages})

def about(request):
    return render(request, 'about.html')

# Use AJAX to display autocomplete search results in the friends page
def autocomplete(request):
  if request.is_ajax():
    user = request.user.id
    friends = FriendConnection.objects.filter(Q(ReceivingUser = user) |
                                              Q(SendingUser = user))
    sending_friends_ids = friends.values('SendingUser')
    receiving_friends_ids = friends.values('ReceivingUser')

    queryset = User.objects.exclude(Q(id__in=sending_friends_ids) | \
     Q(id__in=receiving_friends_ids)) \
    .filter(username__startswith=request.GET.get('search', None))
    list = []
    for i in queryset:
      list.append(i.username)
    data = {
      'list': list
    }
    return JsonResponse(data)



def change_friend_status(request, **kwargs):
  if request.user.is_authenticated:
    if request.method == 'POST':
      # If we aren't adding a friend, then see if we are confirming or deleting
      if not 'add_friend' in request.POST:
        user = request.user
        friendID = kwargs['id']
        friend = FriendConnection.objects.get(id=friendID)
        if 'confirm_friend' in request.POST:
          confirmed = not friend.IsConfirmed
          friend.IsConfirmed = confirmed
          friend.save(update_fields=['IsConfirmed'])
        elif 'delete_friend' in request.POST:
          friend.delete()
      # This is if we are adding a friend
      else:
        try:
          user = User.objects.get(id = kwargs['id'])
          friend = User.objects.get(username = request.POST.get('friend_name', None))
          FriendConnection.objects.create(IsConfirmed=0, SendingUser=user, ReceivingUser = friend)
        except:
          return HttpResponseBadRequest()
    return HttpResponseRedirect("/home/friends/")


class FriendListView(generic.ListView):
  model = FriendConnection
  template_name = 'forum/friend_list.html'
  context_object_name = 'friends'

  def get_queryset(self):
    userID = self.request.user

    return FriendConnection.objects.filter((Q(IsConfirmed=1) & (Q(ReceivingUser_id = userID) | Q(SendingUser_id = userID)))).all()


  def get_context_data(self, *args, **kwargs):
    context = super(FriendListView, self).get_context_data(**kwargs)
    userID = self.request.user
    context['unconfirmed_friends'] = FriendConnection.objects.filter((Q(IsConfirmed=0) &
                                          (Q(ReceivingUser_id = userID) |
                                          Q(SendingUser_id = userID))))
    return context
