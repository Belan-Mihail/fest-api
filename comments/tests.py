from django.contrib.auth.models import User
from post.models import Post
from .models import Comment
from rest_framework import status
from rest_framework.test import APITestCase



class CommentListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
       user = User.objects.create_user(username='user', password='pass')
       post1 = Post.objects.create(owner=user, title='a title')
       post1_comment = Comment.objects.create(owner=user, post_id=1, content='comment')
       post1_comment2 = Comment.objects.create(owner=user, post_id=1, content='comment2')

    
    def test_can_list_post_comments(self):
        user = User.objects.get(username='user')
        post1 = Post.objects.get(title='a title')
        post1_comment = Comment.objects.get(id=1)
        post1_comment2 = Comment.objects.get(id=2)
        response = self.client.get('/comments/')
        count = Comment.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 2)
        self.assertEqual(post1_comment.content, 'comment')
        self.assertEqual(post1_comment2.content, 'comment2')
        self.assertTrue(isinstance(post1_comment, Comment))

    

    def test_cant_list_comments_using_invalid_url(self):
        response = self.client.get('/comment3s/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    

    def test_logged_in_user_can_create_comment(self):
        # self.client.login(username='adam', password='pass') = login immitation
        self.client.login(username='user', password='pass')
        post1 = Post.objects.get(id=1)
        user = User.objects.get(username='user')
        # post creation immitation
        response = self.client.post('/comments/', {'owner': user, 'post': 1, 'content': 'comment3'})
        count = Comment.objects.count()
        post1_comment3 = Comment.objects.get(id=3)
        self.assertEqual(count, 3)
        self.assertEqual(post1_comment3.content, 'comment3')
        # self.assertEqual(obj.title, 'a title1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_not_logged_in_cant_create_comment(self):
        response = self.client.post('/comments/', {'owner': user, 'post': 1, 'content': 'comment4'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
       
       
        
        
    

#     def test_user_not_logged_in_cant_create_post(self):
#         response = self.client.post('/posts/', {'title': 'a title'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class PostDetailViewTests(APITestCase):

#     def setUp(self):
#         adam = User.objects.create_user(username='adam', password='pass')
#         brian = User.objects.create_user(username='brian', password='pass')
#         Post.objects.create(
#             owner=adam, title='a title', content='adams content'
#         )
#         Post.objects.create(
#             owner=brian, title='another title', content='brians content'
#         )
    
#     def test_can_retrieve_post_using_valid_id(self):
#         response = self.client.get('/posts/1/')
#         response2 = self.client.get('/posts/2/')

#         self.assertEqual(response.data['title'], 'a title')
#         self.assertEqual(response.data['owner'], 'adam')
#         self.assertNotEqual(response.data['owner'], 'brian')
#         self.assertEqual(response2.data['owner'], 'brian')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_cant_retrieve_post_using_invalid_id(self):
#         response = self.client.get('/posts/999/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

#     def test_user_can_update_own_post(self):
#         self.client.login(username='adam', password='pass')
#         response = self.client.put('/posts/1/', {'title': 'a new title'})
#         # fetch first post with pk=1 and assign it to the post variable
#         post = Post.objects.filter(pk=1).first()
#         self.assertEqual(post.title, 'a new title')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    # def test_user_cant_update_not_own_post(self):
    #     self.client.login(username='adam', password='pass')
    #     response = self.client.put('/posts/2/', {'title': 'a new title'})
    #     # fetch first post with pk=2 and assign it to the post variable
    #     post = Post.objects.filter(pk=2).first()
    #     self.assertEqual(post.title, 'another title')
    #     self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


