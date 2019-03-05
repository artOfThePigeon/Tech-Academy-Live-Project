from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
import datetime

# Create your views here.
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

        return redirect('login')
    else:
        return render(request, 'Accounts/register.html')