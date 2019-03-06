from django.urls import path

from . import views

app_name = 'Forum'
urlpatterns = [
  path('profile', views.get_profile, name='get_profile')
]
