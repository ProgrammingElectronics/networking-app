from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
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

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# gets all of the profiles in the database
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        
        # Extract comma separated search params, and convert into list
        industry_params = self.request.query_params.get('industry')
        skill_params = self.request.query_params.get('skill')
        bootcamp_params = self.request.query_params.get('bootcamp')
        
        # if no params, return ALL profiles
        if not industry_params and not skill_params and not bootcamp_params:
            return queryset

        # IMPORTANT NOTE: Each indiviudal filter will return ALL matches where ONE of the params is met.  i.e.  If industry params are [Education, Pharma], then any profiles that have either Education or Pharma or both will be returned.  
        #  However -> between filters, we exclude if they don't have both an industry AND a skill. 
       
        # If industry, skill, or bootcamp params are passed...
        # Then apply filters.  
        if industry_params:
            industry_filters = industry_params.split(',')
            queryset = queryset.filter(industries__name__in=industry_filters).distinct()
        
        if skill_params:
            skill_filters = skill_params.split(',')
            queryset = queryset.filter(skills__name__in=skill_filters).distinct()

        if bootcamp_params:
            bootcamp_filters = bootcamp_params.split(',')
            queryset = queryset.filter(enrollment__bootcamp__name__in=bootcamp_filters).distinct()
            
        return queryset


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

