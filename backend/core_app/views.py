from os import access, environ
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConnectionRequestSerializer, EnrollmentSerializer, ProfileSerializer, UserSerializer, BootcampSerializer, UserSerializerWithToken, IndustrySerializer, SkillSerializer
from rest_framework import viewsets
from .models import Bootcamp, ConnectionRequest, Industry, Profile, Skill, Enrollment
from django.db.models import Q
import requests, json




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

# LinkedIn API calls
# This end point takes in the 1st LinkedIn token (referred to as code) from the Frontend
# You combine this code with both keys and make another request for another token.
# Once you have teh 2nd token, you can use that to make API calls to get the linkedIn
# users First Name, Last Name, and Profile Picture
@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
def get_linkedin_id(request):


    print(f'#################### THE CODE #####################: {request.data}')
    # This is the payload to get the 2nd LinkedIn Token.  
    # Code it the value sent via the frontend API call.
    payload = {
        "grant_type": "authorization_code",
        "code": request.data,
        "redirect_uri": 'http://localhost:3000/linkedin',
        "client_id": '7795z7b1o288ud',
        "client_secret": '9rBQfkuJ1Gn3i2DH',
    }

    # This makes the API call to get the 2nd token.
    response_json = requests.get('https://www.linkedin.com/oauth/v2/accessToken', params=payload)
    print(f'#################### token_json.text #####################: {response_json.text}')

    response_dict = json.loads(response_json.text)
    print(f'#################### token_dict #####################: {response_dict}')
    
    access_token = response_dict['access_token']
    print(f'#################### access_token #####################: {access_token}')

    # This is data we'll send back to the frontend that will have the user profile info
    data = {}
    

    headers = {  "Authorization" : f"Bearer {access_token}"}

    data["ID_linkedIn"] = json.loads(requests.get('https://api.linkedin.com/v2/me?projection=(id)', headers=headers).text)['id']
    print(f'#################### data #####################: {data}')
        
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def LinkedIn(request):

    # This is the payload to get the 2nd LinkedIn Token.  
    # Code it the value sent via the frontend API call.
    payload = {
        "grant_type": "authorization_code",
        "code": request.data,
        "redirect_uri": 'http://localhost:3000/linkedin',
        "client_id": '7795z7b1o288ud',
        "client_secret": '9rBQfkuJ1Gn3i2DH',
    }

    # This makes the API call to get the 2nd token.
    response_json = requests.get('https://www.linkedin.com/oauth/v2/accessToken', params=payload)
    print(f'#################### token_json.text #####################: {response_json.text}')

    response_dict = json.loads(response_json.text)
    print(f'#################### token_dict #####################: {response_dict}')
    
    access_token = response_dict['access_token']
    print(f'#################### access_token #####################: {access_token}')

    # This is data we'll send back to the frontend that will have the user profile info
    data = {}
    

    headers = {  "Authorization" : f"Bearer {access_token}"}

    data["ID_linkedIn"] = json.loads(requests.get('https://api.linkedin.com/v2/me?projection=(id)', headers=headers).text)['id']
    data["first_name_linkedIn"] = json.loads(requests.get('https://api.linkedin.com/v2/me?projection=(firstName)', headers=headers).text)['firstName']['localized']['en_US']
    data["last_name_linkedIn"] = json.loads(requests.get('https://api.linkedin.com/v2/me?projection=(lastName)', headers=headers).text)['lastName']['localized']['en_US']
    data["profile_pic_linkedIn"] = json.loads(requests.get('https://api.linkedin.com/v2/me?projection=(profilePicture)', headers=headers).text)['profilePicture']['displayImage']
    print(f'#################### data #####################: {data}')
        
    return Response(data, status=status.HTTP_200_OK)


# REST router viewsets

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

