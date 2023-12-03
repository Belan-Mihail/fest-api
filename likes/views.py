from rest_framework import generics, permissions
from drfapi.permissions import IsOwnerOrReadOnly
from .models import Likes
from .serializers import LikesSerializer

# 46 urls.py create
# 45

class LikesList(generics.ListCreateAPIView):
    """
    List likes or create a like if logged in.
    """
    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Likes.objects.all()


# And just like when we set the user  creating a comment as its owner,  
# we’ll do the same here with a like.  I’ll define the perform_create method,  
# which will take self and serializer  as arguments. When saving the like  
# instance to our database, I’ll set the  owner to be the user making the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a likes or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()