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
        return instance

    class Meta:
        model = User
        fields = [
            'token', 'username', 'password'
            ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'education', 'is_professional', 'phone_number', 'linkedin_url', 'github_url', 'img_url', 'about_me'
        ]


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = [
            'id', 'name', 'size'
            ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'type'
            ]



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
            'id', 'from_profile', 'to_profile'
            ]

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id', 'profile', 'bootcamp', 'graduation_year', 'graduation_status'
            ]