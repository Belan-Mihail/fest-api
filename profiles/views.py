from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drfapi.permissions import IsOwnerOrReadOnly

# 6 
# 7 create urls.py in profiles
# 10 import serialize and edit profile model


# This is the reason we saw the error. The profiles  can’t be just thrown in as a part of the Response,  
# we need a serializer to convert Django model  instances to JSON

class ProfileList(APIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """
    def get(self, request):
        profiles = Profile.objects.all()
        # return Response(profiles)

        # 10
#         Before we return a Response, we’ll create  a ProfileSerializer instance.
# We’ll pass in profiles and many equals True, to specify  we’re serializing multiple Profile instances.
        
        # before 19
        # serializer = ProfileSerializer(profiles, many=True)
        # 19
        serializer = ProfileSerializer(
            profile, context={'request': request}, many=True
        )
        return Response(serializer.data)


# 11 and import Http404
class ProfileDetail(APIView):
    # below this class
    # 14
#     If we explicitly set the serializer_class attribute  on our ProfileDetail view, the rest framework  
# will automatically render a form for us, based on  the fields we defined in our ProfileSerializer.
# add normal fields to update content

    serializer_class = ProfileSerializer

    # 18
    permission_classes = [IsOwnerOrReadOnly]

    # 11
    def get_object(self, pk):
        
        try:
            profile = Profile.objects.get(pk=pk)
            # 18 and from drfapi.permissions import IsOwnerOrReadOnly
            # 19add context={'request': request} to all serizlized methond in all class (up and down)
            # 20 serialized
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    
# 11
# 12 urls.py
    def get(self, request, pk):
        profile = self.get_object(pk)
        # Then, I’ll call our ProfileSerializer with the  profile instance. No need to pass in many=True,  
# as unlike last time, we’re dealing with a single  profile model instance and not a queryset.
        
        # before 19
        # serializer = ProfileSerializer(profiles)
        # 19
        serializer = ProfileSerializer(
            profile, context={'request': request}
        )
        return Response(serializer.data)
    
    # 13 and from rest_framework import status
    def put(self, request, pk):
        profile = self.get_object(pk)
        

        # before 19
        # serializer = ProfileSerializer(profiles, data=request.data)
        # 19
        serializer = ProfileSerializer(
            profile, context={'request': request}, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 14 up to Profile detail

    # 15 create second auperuser
    # 16 urls.py drfapi