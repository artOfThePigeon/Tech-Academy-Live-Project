from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
import datetime
from .models import Comment, UserProfile, Topic, Thread

# Create your views here.

def home_view(request):
    #collect data for latest 10 threads on homepage
   data = Thread.objects.values().order_by('-DateUpdate')[:10] 
   #convert to dictionary to pass variable
   threads = {"threads" : data}       
   return render(request, 'index.html', threads)


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

