from django.contrib import admin
from .models import Profile, Industry, Experience 
# Register your models here.

models = [Profile, Industry, Experience]
admin.site.register(models)