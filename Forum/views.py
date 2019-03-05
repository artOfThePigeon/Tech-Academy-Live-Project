from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.
def register(request): # each view function takes an HttpRequest object as a parameter.


    #  -- This view handler is used two times in the use-case of registering a user.  On initial load, your first visit to the page, there is no posted data and consequently it queries the DB for 
    #contextual data to populate and create a view page for the user to enter data.  First or second visit to this handler is indicated by using the request.method to determine if a user clicked
    #on a link or POSTed from a form.


    if request.method == 'POST': #This branch is for retreiving user input

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        u1 = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password) # this also returns a user object which...
        u1.save() # then we can save the changes to the database.

        return redirect('login') # this currently redirects the user back to the homepage, potentially this can redirect a new user to a dashboard, etc.
