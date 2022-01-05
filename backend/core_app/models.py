from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='profile')
    education = models.CharField(max_length=250)
    is_professional = models.BooleanField(blank=True)
    phone_number = models.CharField(max_length=10)
    linkedin_url = models.CharField(max_length=250, blank=True)
    github_url = models.CharField(max_length=250, blank=True)
    img_url = models.CharField(max_length=250, blank=True)
    about_me = models.TextField(max_length=1000, blank=True)
    # bootcamp
    # skills
    # industry

    def __str__(self):
        return f'Profile ID: {self.id} User: {self.user}'


class Industry(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Industry ID: {self.id} Name: {self.name}'

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=CASCADE, related_name="experience")
    industry = models.ForeignKey(Industry, on_delete=CASCADE, related_name="experience")
    years = models.IntegerField(blank=True)
    #TODO - Add Skill as FK related

    def __str__(self):
        return f'Experience ID: {self.id} Profile ID: {self.profile} Industry ID: {self.industry}'