from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

CONNECTION_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

YEAR_CHOICES = (
    ('0-1', '0-1 Years'),
    ('1-3', '1-3 Years'),
    ('3-0', '3-Up Years'),
)

GRADUATION_STATUS = (
    ('enrolled', 'Enrolled'),
    ('graduated', 'Graduated'),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=CASCADE, related_name='profile')
    education = models.CharField(max_length=250, blank=True)
    is_professional = models.BooleanField(blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    linkedin_url = models.CharField(max_length=250, blank=True)
    github_url = models.CharField(max_length=250, blank=True)
    img_url = models.CharField(max_length=250, blank=True)
    about_me = models.TextField(max_length=1000, blank=True)
    # Group may not need this due to the connection request model
    # connections = models.ManyToManyField('self', blank=True, related_name='connections')

    def __str__(self):
        return f'Profile ID: {self.id} User: {self.user}'


class Industry(models.Model):
    profiles = models.ManyToManyField(Profile, blank=True, related_name="industries")
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Industry ID: {self.id} Name: {self.name}'


class Skill(models.Model):
    profiles = models.ManyToManyField(Profile, blank=True, related_name="skills")
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Skill ID: {self.id} Name: {self.name}'


class Bootcamp(models.Model):
    name = models.CharField(max_length=255, blank=True)
        
    def __str__(self):
        return f'Bootcamp ID: {self.id} Name: {self.name}'


class Enrollment(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="enrollment", blank=True)
    bootcamp = models.ForeignKey(
        Bootcamp, on_delete=CASCADE, related_name="enrollment", blank=True)
    graduation_year = models.CharField(max_length=4, blank=True)
    graduation_status = models.CharField(max_length=255, choices=GRADUATION_STATUS, blank=True)

    # added blank=True  to graduation status
    # TODO graduation year should be a Date

    def __str__(self):
        return f'Enrollment ID: {self.id} Bootcamp ID: {self.bootcamp} Profile ID: {self.profile} Status: {self.graduation_status}'


# This should hold pending requests, the status determines whether it has been denied/approved/pending
class ConnectionRequest(models.Model):
    # for POST this should grab the user id of current user
    from_profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="from_profile")
    to_profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="to_profile")
    status = models.CharField(max_length=255, choices=CONNECTION_STATUS, default='pending')
   
    def __str__(self):
        return f'Connection ID: {self.id} From User: {self.from_profile} To User: {self.to_profile} Status: {self.status}'