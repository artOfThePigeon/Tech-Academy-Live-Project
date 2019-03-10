from django.test import TestCase
from .views import CommentThread
from django.contrib.auth.models import User
from django.test import RequestFactory
# Create your tests here.
'''
class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        '''


request_factory = RequestFactory()
my_url = '/my_full/url/here'  # Replace with your URL -- or use reverse
my_request = request_factory.get(my_url)
user = User.objects.get(pk=1)
response = CommentThread.as_view()(my_request, pk=8, user = user)  # Replace with your view
response.render()
print(dir(response.json()))
