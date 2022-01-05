from django.contrib import admin
from .models import Profile, Industry, Skill, Experience, Bootcamp
# Register your models here.

models = [Profile, Industry, Skill, Experience, Bootcamp]
admin.site.register(models)