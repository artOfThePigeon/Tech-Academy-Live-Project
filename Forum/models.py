from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from TTA import settings
import os


def user_directory_path(instance, filename):
  # TODO: Upload to media/user_<id>/avatar/<filename>
  #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  return 'avatar/user_{0}/{1}'.format(instance.User.id, filename)

class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Signature = models.CharField(max_length=200, null=True)
    Avatar = models.ImageField(upload_to = user_directory_path, blank=True, default='avatar/default-avatar.png')

    def __str__(self):
        """String for replacing the default 'UserProfile object 1' formatting """
        return f'{self.User.username} Profile'

    @classmethod
    def updateProfile(self, request, form):
      # We need to see if the user is logged in before they update their profile.
      user = request.user
      if user.is_authenticated:
        userID = user.id
        sig = form['Signature']
        #if the Avatar field is empty, value will be false, otherwise ImageFile
        avatar = request.FILES['Avatar'] if 'Avatar' in request.FILES else False
        try:
          # I think we should create a UserProfile object on account registration.
          UserProfile.objects.create(User=User.objects.get(User_id=userID), Signature=sig, Avatar=avatar )
        except:
          # Otherwise update the database
          profile = UserProfile.objects.get(User_id = userID)
          profile.Signature = sig
          # if the Avatar field wasn't empty, do stuff
          if avatar != False:
            avatar_url = profile.Avatar.url
            # if the current avatar url DOES NOT match the default,
            # delete the old avatar then create the new one
            if not avatar_url.endswith('/media/avatar/default-avatar.png'):
              if os.path.isfile(settings.BASE_DIR + avatar_url):
                os.remove(settings.BASE_DIR + avatar_url)
            profile.Avatar = avatar
          profile.save()

      else:
        #  ask them to register (or login?) if their user doesn't authenticate
        HttpResponseRedirect('/register/')


class Topic(models.Model):
    TopicTitle = models.CharField(max_length=100)
    DateUpdated = models.DateField()
    ThreadCount = models.IntegerField()

    def __str__(self):
      return self.TopicTitle

class Thread(models.Model):
    ThreadTitle = models.CharField(max_length=100)
    ThreadBody = models.CharField(max_length=1000)
    Author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ViewCount = models.IntegerField()
    Topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    DateStarted = models.DateField()
    PostCount = models.IntegerField()
    DateUpdate = models.DateField()
    UpVoteCount = models.IntegerField(default=0)

    class Meta:
      ordering = ['-DateUpdate']

class Comment(models.Model):
    User = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    Thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    CommentBody = models.CharField(max_length=1000)
    DateCreated = models.DateTimeField(auto_now=True)


class FriendConnection(models.Model):
    ReceivingUser = models.ForeignKey(User,related_name="FriendReceiver", on_delete=models.CASCADE)
    SendingUser = models.ForeignKey(User,related_name="FriendSender", on_delete=models.CASCADE)
    IsConfirmed = models.BooleanField()

class Message(models.Model):
    ReceivingUser = models.ForeignKey(User,related_name="MessageReceiver", on_delete=models.CASCADE)
    SendingUser = models.ForeignKey(User,related_name="MessageSender", on_delete=models.CASCADE)
    Subject = models.CharField(max_length=50)
    MessageBody = models.CharField(max_length=1000)
    DateSent = models.DateTimeField(auto_now=True)

class Upvote(models.Model):
  User = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  Thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
