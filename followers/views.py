from rest_framework import generics, permissions
from drfapi.permissions import IsOwnerOrReadOnly
from .models import Followers
from .serializers import FollowersSerializer

# 50 urls.py create
# 49

class FollowersList(generics.ListCreateAPIView):
    """
    List followers or create a like if logged in.
    """
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Followers.objects.all()


# And just like when we set the user  creating a comment as its owner,  
# we’ll do the same here with a like.  I’ll define the perform_create method,  
# which will take self and serializer  as arguments. When saving the like  
# instance to our database, I’ll set the  owner to be the user making the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowersDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a followers or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowersSerializer
    queryset = Followers.objects.all()