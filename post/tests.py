from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

# 38 startapp comments and add to settings.py go to the model

# 37
class PostListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    
# Now, let’s test that we can list  posts present in the database.
# First, I’ll get the user adam which  we just created in the setUp method,  
# so that I can associate the newly  created post with that user.
# What I want to test now, is that I can make a  get request to ‘/posts’ to list all the posts.  
# !!!!!!!!!!!!You make test network requests by calling  an appropriate method on self-dot-client,  
# !!!!!!!!!!!!namely self.client.get  or .post, .put, and so on,  
# !!!!!!!!!!!!followed by the url we’re making the request to.  
    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        obj = Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.title, 'a title')
        self.assertEqual(len(response.data), 1)
        self.assertTrue(isinstance(obj, Post))
        print(response.data)
        print(obj.title)
        print(len(response.data))
    

    def test_cant_list_posts_using_invalid_url(self):
        response = self.client.get('/posts12345/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_logged_in_user_can_create_post(self):
        # self.client.login(username='adam', password='pass') = login immitation
        self.client.login(username='adam', password='pass')
        # post creation immitation
        response = self.client.post('/posts/', {'title': 'a title1'})
        count = Post.objects.count()
        obj = Post.objects.get()
        self.assertEqual(count, 1)
        self.assertEqual(obj.title, 'a title1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
    

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):

    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )
    
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        response2 = self.client.get('/posts/2/')

        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.data['owner'], 'adam')
        self.assertNotEqual(response.data['owner'], 'brian')
        self.assertEqual(response2.data['owner'], 'brian')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetch first post with pk=1 and assign it to the post variable
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_user_cant_update_not_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        # fetch first post with pk=2 and assign it to the post variable
        post = Post.objects.filter(pk=2).first()
        self.assertEqual(post.title, 'another title')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

