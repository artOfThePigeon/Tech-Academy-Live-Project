from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Signature = models.CharField(max_length=200, null=True)
    Avatar = models.ImageField(upload_to = 'user_avatar/',
      default = 'pic_folder/None/no-img.jpb', null=True)

    # We need to see if the user is logged in before they update their profile.
    @classmethod
    def updateProfile(self, request, form):
      user = request.user
      if user.is_authenitcated():
        userID = user.id

        try:
          UserProfile.create(User_id=userID )
        except:
          # TODO: make a meaningful error message
          print('Something went wrong')
      else:
        # TODO: ask them to register or something
        print("You're not logged in!")


    def __str__(self):
        """String for replacing the default 'UserProfile object 1' formatting """
        return self.User.username


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
