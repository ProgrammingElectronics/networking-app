from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConnectionRequestSerializer, EnrollmentSerializer, ProfileSerializer, UserSerializer, BootcampSerializer, UserSerializerWithToken, IndustrySerializer, SkillSerializer
from rest_framework import viewsets
from .models import Bootcamp, ConnectionRequest, Industry, Profile, Skill, Enrollment
from django.db.models import Q

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


class BootcampViewSet(viewsets.ModelViewSet):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerializer

# connectionRequestViewSet is now set to only access objects where the profile is the from_profile
class ConnectionRequestViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user.id
        profile = Profile.objects.get(user_id=user)
        return ConnectionRequest.objects.filter(
            Q(from_profile=profile) | Q(to_profile=profile)
        )

    serializer_class = ConnectionRequestSerializer
    ordering_fields = ['status']


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

