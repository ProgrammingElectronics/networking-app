from django.contrib import admin
from .models import Profile, Industry, Skill, Experience, Bootcamp, ConnectionRequest
# Register your models here.

models = [Profile, Industry, Skill, Experience, Bootcamp, ConnectionRequest]
admin.site.register(models)