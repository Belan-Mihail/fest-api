
from django.http import Http404
from rest_framework import status, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wall
from .serializers import WallSerializer
from drfapi.permissions import IsOwnerOrReadOnly


class WallList(generics.ListCreateAPIView):

    serializer_class = WallSerializer
    queryset = Wall.objects.all()
     

 
class WallDetail(generics.RetrieveAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WallSerializer
    queryset = Wall.objects.all()
