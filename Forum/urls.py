from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Forum'
urlpatterns = [
  path('register/', views.register, name='register'),
  path('profile/', views.get_profile, name='get_profile'),
  path('message', views.message, name='message'),
  path('inbox', views.inbox, name='inbox'),
  path('msg_detail', views.messagedetails, name='messagedetail'),
  path('topics/', views.TopicsView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
