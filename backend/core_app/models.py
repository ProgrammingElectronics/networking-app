from django.db import models
from django.contrib.auth.models import User
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

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=CASCADE, related_name='profile')
    education = models.CharField(max_length=250)
    is_professional = models.BooleanField(blank=True)
    phone_number = models.CharField(max_length=10)
    linkedin_url = models.CharField(max_length=250, blank=True)
    github_url = models.CharField(max_length=250, blank=True)
    img_url = models.CharField(max_length=250, blank=True)
    about_me = models.TextField(max_length=1000, blank=True)
    connections = models.ManyToManyField('self', blank=True, related_name='connections')

    def __str__(self):
        return f'Profile ID: {self.id} User: {self.user}'


class Industry(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Industry ID: {self.id} Name: {self.name}'


class Skill(models.Model):
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Skill ID: {self.id} Name: {self.name}'


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="experience")
    industry = models.ForeignKey(
        Industry, on_delete=CASCADE, related_name="experience")
    years = models.CharField(blank=True, max_length=255, choices=CONNECTION_STATUS)
    skill = models.ForeignKey(
        Skill, on_delete=CASCADE, related_name="experience")

    def __str__(self):
        return f'Experience ID: {self.id} Profile ID: {self.profile} Industry ID: {self.industry} Skill ID: {self.skill}'


class Bootcamp(models.Model):
    name = models.CharField(max_length=255, blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="bootcamp")
        
    def __str__(self):
        return f'Bootcamp ID: {self.id} Name: {self.name}'


# This should hold pending requests, the status determines whether it has been denied/approved/pending
class ConnectionRequest(models.Model):
    # for POST this should grab the user id of current user
    from_profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="from_user")
    to_profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name="to_user")
    status = models.CharField(max_length=255, choices=CONNECTION_STATUS, default='pending')

    
    def __str__(self):
        return f'Connection ID: {self.id} From User: {self.from_user} To User: {self.to_user} Status: {self.status}'