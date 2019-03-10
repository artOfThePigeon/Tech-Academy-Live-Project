from django.urls import path, re_path
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
  path('topics/', views.TopicsView.as_view(), name='topics'),
  path('thread/<slug:pk>/', views.CommentThread.as_view(), name='thread'),
  re_path(r'^thread/(?P<slug>\w+)/comment$', views.create_comment, name='post_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
