from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Forum'
urlpatterns = [
  path('profile/', views.get_profile, name='get_profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
