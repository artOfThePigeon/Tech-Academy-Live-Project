from django.urls import path

from . import views

app_name = 'Forum'
urlpatterns = [
  path('', views.get_profile, name='user_profile')
]
