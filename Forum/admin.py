from django.contrib import admin

from Forum.models import UserProfile
# Register your models here.

# Define the admin class
class UserProfileAdmin(admin.ModelAdmin):
  pass

#Register the admin class witht he associated model
admin.site.register(UserProfile, UserProfileAdmin)
