from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drfapi.permissions import IsOwnerOrReadOnly

# create urls.py in posts
# 29
# class PostList(APIView):
    # 34 add PostDetailView with get and put
    # 33
    # To have a nice create post form  rendered in the preview window,  
# let’s also set the serializer_class attribute  to PostSerializer on our PostList class.
    # serializer_class = PostSerializer

    # import permissions
    # This permission checks whether the user is authenticated when receiving a record 
    # (it is built into the restframework and only needs to be imported and registered),
    #  which is necessary to create a new record
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly
    # ]

    # 33-!

    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(
    #         posts, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # 33 up
    # 32
    # def post(self, request):
        # I’ll deserialize the post data,  
# passing in whatever the user sends in the request  and the request itself in the context object.
        # serializer = PostSerializer(
        #     data=request.data, context={'request': request}
        # )
        # if serializer.is_valid():
# I’ll call the save method on the serializer and  pass in the user that is making the request.
        #     serializer.save(owner=request.user)
        #     return Response(
        #         serializer.data, status=status.HTTP_201_CREATED
        #     )
        # return Response(
        #     serializer.errors, status=status.HTTP_400_BAD_REQUEST
        # )
    # 32-!

# 35 urls.py
    # 34 import Http404 and from drfapi.permissions import IsOwnerOrReadOnly
# class PostDetail(APIView):

#     serializer_class = PostSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             post = Post.objects.get(pk=pk)
#             self.check_object_permissions(self.request, post)
#             return post
#         except Post.DoesNotExist:
#             raise Http404
    

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(
#             post, context={'request': request}
#         )
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         post = self.get_object(pk)

#         serializer = PostSerializer(
#             post, context={'request': request}, data=request.data
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 34-!

# 37 test post
# 36
    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )
# 36!
    
class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()