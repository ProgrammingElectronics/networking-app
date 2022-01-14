from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Enrollment, Industry, Profile, Skill, Bootcamp, ConnectionRequest


# Serializes current user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'profile']
        

# To be used when this is the bottom of the nested serializer
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name',
                  'last_name', 'email']


# This is the more generic profile serializer that only responds with some of the data. This is more publically consumable
class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'img_url', 
        ]


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = [
            'id', 'name', 'size', 'profiles'
            ]


class EndNestedIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = [
            'name', 'size'
            ]
    depth = 1


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'type', 'profiles'
            ]


class EndNestedSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'name', 'type'
            ]
    depth = 1


class BootcampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = [
            'id', 'name'
            ]


class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = [
            'id', 'from_profile', 'to_profile', 'status'
            ]


class EnrollmentSerializer(serializers.ModelSerializer):
    
    bootcamp = BootcampSerializer()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'profile', 'bootcamp', 'graduation_year', 'graduation_status'
            ]
        
class EndNestedEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'bootcamp', 'graduation_year', 'graduation_status'
            ]
        depth = 1


class ProfileSerializer(serializers.ModelSerializer):
    # This limits the information coming back from the user to not include the password 
    user = PublicUserSerializer(read_only=True)
    
    enrollment = EnrollmentSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    industries = IndustrySerializer(many=True, read_only=True)


    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'education', 'is_professional', 'phone_number', 'linkedin_url', 'github_url', 'img_url', 'about_me', 'enrollment', 'skills', 'industries'
        ]


# Serializes new user sign ups that responds with the new user's information including a new token.
class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        print(instance.id)
        Profile.objects.create(user=instance, education='', is_professional=False, phone_number='', linkedin_url='', github_url='', img_url='', about_me='')
        return instance

    class Meta:
        model = User
        fields = [
            'id', 'token', 'username', 'password'
            ]
