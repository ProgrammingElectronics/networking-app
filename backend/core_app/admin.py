from django.contrib import admin
from .models import Profile, Industry, Skill, Experience
# Register your models here.

models = [Profile, Industry, Skill, Experience]
admin.site.register(models)