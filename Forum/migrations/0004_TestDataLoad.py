from django.db import migrations
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import random

def load_data(apps, schema_editor):
    # 'apps' refers to the application registry API
    #       the Schema Editor is part of the data abstraction layer of the migration system that
    #       takes our Python methods and turns them into SQL.

    #  Key Notes
    #     1) When inserting dates its best to use django.utils.timezone
    #     2) Test data is created with naming patterns for create/delete correctly.
    #           DO NOT CHANGE the pattern unless you change it everywhere.
    #

    userData = {}

    # Instantiate and create 20 Users
    for i in range(1, 21):
        user = User.objects.create_user(
            first_name="TestFirst_" + str(i),
            last_name="TestLast_" + str(i),
            password='Pass1234!',
            email="TestFirst{}_TestLast{}@example.com".format(i, i),
            username="test_user_{}".format(i),
            is_staff=True if i > 16 else False,
            is_active=True if i > 1 else False,
            date_joined=timezone.now() - datetime.timedelta(minutes=random.randint(3, 50000)),
            last_login= timezone.now() + datetime.timedelta(minutes=random.randint(3, 1000)),
        )
        user.save()
        userData[i] = {
            'id': user.id,
        }

    # Instantiate and create 20 UserProfiles for the users created above.
    UserProfile = apps.get_model('Forum', 'UserProfile')
    for i in range(1, 21):
        user_profile = UserProfile(
            User_id=userData[i]['id'],
            Signature="TestSignature_{}".format(i),
            Avatar = 'avatar/default-avatar.png'
        )
        user_profile.save()

    # Make the first 10 users friends with another user in the next 10.
    FriendConnection = apps.get_model('Forum', 'FriendConnection')
    for i in range(1, 11):
        friend_connection = FriendConnection(SendingUser_id=userData[i]['id'], ReceivingUser_id=userData[i + 10]['id'], IsConfirmed=True)
        friend_connection.save()

    # Create 10 messages from the first 10 users to a user in the next 10.
    Message = apps.get_model('Forum', 'Message')
    for i in range(1, 11):
        message = Message(
            Subject="Test Message from est_user_{} to est_user_{}".format(i, i+10),
            MessageBody="Test Message Body from est_user_{} to est_user_{}".format(i, i+10),
            DateSent= timezone.now(),
            SendingUser_id=userData[i]['id'],
            ReceivingUser_id=userData[i+10]['id'],
            )
        message.save()

    # Create 5 Topics, 25 Threads, and  50 Comments
    Thread = apps.get_model('Forum', 'Thread')
    Topic = apps.get_model('Forum', 'Topic')
    Comment = apps.get_model('Forum','Comment')
    for i in range(1, 6):
        topic = Topic(
            TopicTitle="Test Topic Number {}".format(i),
            DateUpdated=timezone.now() - datetime.timedelta(minutes=random.randint(3, 1000)),
            ThreadCount=(i + 2),
        )
        topic.save()
        # Make i+2 Threads for each Topic.  This will give some variety to the Topic section lengths in the view.
        for y in range(i + 2):
            author_num = random.randint(1,20)
            thread = Thread(
                ThreadTitle="Thread title {}:{}".format(i, y),
                ThreadBody="This is the thread body of {}:{}".format(i, y),
                ViewCount=0,
                DateStarted=timezone.now() - datetime.timedelta(minutes=random.randint(3, 20000)),
                PostCount=2,
                DateUpdate=timezone.now() + datetime.timedelta(minutes=random.randint(3, 1000)),
                Author_id=userData[author_num]['id'],
                Topic_id=topic.id,
            )
            thread.save()
            # Make 2 Comments for each thread.
            for z in range(1, 3):
                comment_author_num = random.randint(1,  20)
                comment = Comment(
                    CommentBody="This is comment {} of thread {}".format(z, thread.ThreadTitle),
                    DateCreated=timezone.now(),
                    Thread_id=thread.id,
                    User_id=userData[comment_author_num]['id'],
                )
                comment.save()


def delete_data(apps, schema_editor):
    # The Deletion

    # Delete the Test Users.  The other objects are defined to cascade delete in the models.py
    User.objects.filter(first_name__startswith='TestFirst_').delete()
    # Delete Test Topics.  Threads and Comments are deleted are defined to cascade delete in the models.py
    Topic = apps.get_model('Forum', 'Topic')
    Topic.objects.filter(TopicTitle__startswith='Test Topic Number').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0003_auto_20190301_1136'),
    ]

    operations = [
        migrations.RunPython(load_data, delete_data),
    ]
