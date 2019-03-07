from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
  #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  return 'avatar/user_{0}/{1}'.format(instance.User.id, filename)

class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Signature = models.CharField(max_length=200, null=True)
    Avatar = models.ImageField(upload_to = user_directory_path, blank=True, default='avatar/default-avatar.png')

    def __str__(self):
        """String for replacing the default 'UserProfile object 1' formatting """
        return f'{self.User.username} Profile'

    # We need to see if the user is logged in before they update their profile.
    @classmethod
    def updateProfile(self, request, form):
      # TODO: Delete old profile pics or reuse old pictures
      user = request.user
      if user.is_authenticated:
        userID = user.id
        sig = form['Signature']
        avatar = request.FILES['Avatar'] if 'Avatar' in request.FILES else False
        try:
          UserProfile.objects.create(User=User.objects.get(User_id=userID), Signature=sig, Avatar=avatar )
        except:
          # Update the database
          profile = UserProfile.objects.get(User_id = userID)
          profile.Signature = sig
          if avatar != False:
            profile.Avatar = avatar
          profile.save()

      else:
        # TODO: ask them to register or something
        print("You're not logged in!")


# Trying to upload the avatar file
class ImageFile(models.Model):
    img_file = models.ImageField(upload_to='avatars/%Y/%m/%d')

class Topic(models.Model):
    TopicTitle = models.CharField(max_length=100)
    DateUpdated = models.DateField()
    ThreadCount = models.IntegerField()

class Thread(models.Model):
    ThreadTitle = models.CharField(max_length=100)
    ThreadBody = models.CharField(max_length=1000)
    Author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ViewCount = models.IntegerField()
    Topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    DateStarted = models.DateField()
    PostCount = models.IntegerField()
    DateUpdate = models.DateField()

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
