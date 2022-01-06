from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConnectionRequestSerializer, ProfileSerializer, UserSerializer, BootcampSerializer, UserSerializerWithToken, IndustrySerializer, SkillSerializer, ExperienceSerializer
from rest_framework import viewsets
from .models import Bootcamp, ConnectionRequest, Industry, Profile, Skill, Experience

## The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to.
@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# REST router viewsets

# gets all of the profiles in the database
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class BootcampViewSet(viewsets.ModelViewSet):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer


class ConnectionRequestViewSet(viewsets.ModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer

