from django.db.models import Count
from django.http import Http404
from rest_framework import status, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drfapi.permissions import IsOwnerOrReadOnly
from followers.models import Followers

# 6 
# 7 create urls.py in profiles
# 10 import serialize and edit profile model


# This is the reason we saw the error. The profiles  can’t be just thrown in as a part of the Response,  
# we need a serializer to convert Django model  instances to JSON

# class ProfileList(APIView):

    # def get(self, request):
    #     profiles = Profile.objects.all()
        # return Response(profiles)

        # 10
#         Before we return a Response, we’ll create  a ProfileSerializer instance.
# We’ll pass in profiles and many equals True, to specify  we’re serializing multiple Profile instances.
        
        # before 19
        # serializer = ProfileSerializer(profiles, many=True)
        # 19
        # serializer = ProfileSerializer(
        #     profiles, context={'request': request}, many=True
        # )
        # return Response(serializer.data)


# 11 and import Http404
# class ProfileDetail(APIView):
    # below this class
    # 14
#     If we explicitly set the serializer_class attribute  on our ProfileDetail view, the rest framework  
# will automatically render a form for us, based on  the fields we defined in our ProfileSerializer.
# add normal fields to update content

    # serializer_class = ProfileSerializer

    # 18
    # permission_classes = [IsOwnerOrReadOnly]

    # failed!
    # my own experement from 33 steps. Add thats only Authenticated users can watch profile detail
    # need import from rest_framework import status, permissions
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly
    # ] 

    # 11
    # def get_object(self, pk):
    #     try:
    #         profile = Profile.objects.get(pk=pk)
            # 18 and from drfapi.permissions import IsOwnerOrReadOnly
            # 19add context={'request': request} to all serizlized methond in all class (up and down)
            # 20 serialized
        #     self.check_object_permissions(self.request, profile)
        #     return profile
        # except Profile.DoesNotExist:
        #     raise Http404
    
# 11
# 12 urls.py
    # def get(self, request, pk):
    #     profile = self.get_object(pk)
        # Then, I’ll call our ProfileSerializer with the  profile instance. No need to pass in many=True,  
# as unlike last time, we’re dealing with a single  profile model instance and not a queryset.
        
        # before 19
        # serializer = ProfileSerializer(profiles)
        # 19
        # serializer = ProfileSerializer(
        #     profile, context={'request': request}
        # )
        # return Response(serializer.data)
    
    # 13 and from rest_framework import status
    # def put(self, request, pk):
    #     profile = self.get_object(pk)
        

        # before 19
        # serializer = ProfileSerializer(profiles, data=request.data)
        # 19
        # serializer = ProfileSerializer(
        #     profile, context={'request': request}, data=request.data
        # )
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 14 up to Profile detail

    # 15 create second auperuser
    # 16 urls.py drfapi


class ProfileList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """
    serializer_class = ProfileSerializer

    # The annotate function allows  us to define extra fields to be added to the  
# queryset.

# We can see, however, that there is no direct  relationship between Profile and Post.  
# That’s why we need to go through  the User model to get there. 
# So, inside the Count class, we will need  to perform a lookup that spans the profile,  
# user, and post models, so we can get to the  Post model with the instances we want to count.
    queryset = Profile.objects.annotate(
        # how many post user has

#         Similar to when we used dot notation,  the first part of our lookup string  
# is the owner field on the Profile model,  which is a OneToOne field referencing User.  
# From there we can reach the  Post model. So we have to add  
# ‘double underscore post’ to show the  relationship between Profile, User and Post.

# As we’ll be defining more than one field  inside the annotate function, we also need to  
# pass distinct=True here to only count the unique  posts. Without this we would get duplicates.
        posts_count=Count('owner__post', distinct=True),

#         This time we have a problem. Within the  Follower model, we have two foreign keys  
# that are referencing the User model. One  to identify the User following another user  
# and the other to identify the one being followed.  So here, we need to use the related_names  
# “following” and “followed” defined in followers’  models.py file, instead of  
# the model name like we did for owner__post. The  string value then, will be ‘owner__followed’.  
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')

# review
# So, just to review what we’ve done here.  First, we’ve used the annotate method on  
# Profile to add some specific fields to our  queryset. We’ve then used the count method  
# to calculate how many model instances of each  there are. We’ve linked these fields to their  
# relevant model fields, and limited our instances  being returned using distinct = True.


#     Next, we’ll need to create our filters. To make these fields sortable,  
# I’ll set the filter_backends  attribute to OrderingFilter.
# I’ll also need to set the ordering_fields  to the fields we just annotated,  
# namely posts, followers and following count.

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]


    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]


    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
#         I’d also like to be able to sort our profiles by  how recently they followed a profile and by how  
# recently they have been followed by a profile.  We’ll use the ‘created_at’ field to do this,  
# and then just attach this to the following and  followed related name fields, as appropriate.
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
