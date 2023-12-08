from rest_framework import generics, permissions
from drfapi.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend

# 41 urls.py comments
# 40
# As we want to both list and create comments in the  ListView, instead of explicitly defining the post  
# and get methods like we did before,  I’ll extend generics’ ListCreateAPIView.  
# Extending the ListAPIView means we  won’t have to write the get method  
# and the CreateAPIView takes  care of the post method.
# It’s worth pointing out that  if you need a different view,  
# you can always use the autocomplete feature.  It lists all the available generic APIView  
# classes in a nice menu
# generics.ListCreateAPIView for GET and POST methods
class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """
    # We’ll have to set the serializer_class to  CommentSerializer and permission_classes to  
# IsAuthenticatedOrReadOnly as we don’t  want anonymous users to comment.
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     Instead of specifying only the model we’d like  to use, in DRF we set the queryset attribute.  
# This way, it is possible to filter  out some of the model instances.  
# This would make sense if we were  dealing with user sensitive data  
# like orders or payments where we would need to  make sure users can access and query only their own data.
    queryset = Comment.objects.all()

    filter_backends = [
        DjangoFilterBackend
    ]


    filterset_fields = [
        'post'
    ]

#     Before we test the view, we’ll have to make sure  comments are associated with a user upon creation.  
# We do this with generics by  defining the perform_create method,  
# which takes in self and serializer as arguments.  Inside, we pass in the user making the request as  
# owner into the serializer’s save method, just  like we did in the regular class based views.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# More good news is that with generics, the request  is a part of the context object by default.  
# What this means is that we no  longer have to pass it manually,  
# like we did in the regular class based views.
# we dont need context={'request': request}

# Now, the CommentDetail view.  As we’d like to retrieve,  
# update and delete a comment, I’ll extend  the RetrieveUpdateDestroyAPI generic view.
# We want only the comment owner to be able to edit  or delete it, so I’ll set the permission_classes  
# to IsOwnerOrReadOnly. In order not to have to send  the post id every time I want to edit a comment,  
# I’ll set serializer_class  to CommentDetailSerializer.  
# Queryset will remain the same.
# Our serializer still needs to access the request,  but as mentioned before, we don’t really need to  
# do anything, as the request is passed in  as part of the context object by default.
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
