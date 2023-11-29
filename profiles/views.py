from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

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
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

