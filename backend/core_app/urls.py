from django.urls import path
from .views import ProfileViewSet, current_user, UserList
from rest_framework.routers import DefaultRouter

# create router for views
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view())
]

# adds all of our urls together/custom and rest framework
urlpatterns += router.urls