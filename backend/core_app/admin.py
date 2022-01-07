from django.contrib import admin
from .models import Enrollment, Profile, Industry, Skill, Bootcamp, ConnectionRequest
# Register your models here.

models = [Profile, Industry, Skill, Bootcamp, ConnectionRequest, Enrollment]
admin.site.register(models)