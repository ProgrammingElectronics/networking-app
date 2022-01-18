from django.urls import path
from .views import UserViewSet, ConnectionRequestViewSet, EnrollmentViewSet, ProfileViewSet, current_user, BootcampViewSet, UserList, IndustryViewSet, SkillViewSet, EditProfileViewSet, AddEnrollmentViewSet
from rest_framework.routers import DefaultRouter

# create router for views
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'edit-profiles', EditProfileViewSet, basename='edit-profiles')
router.register(r'industries', IndustryViewSet, basename='industries')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'bootcamps', BootcampViewSet, basename='bootcamps')
router.register(r'connection-requests', ConnectionRequestViewSet, basename='requests')
router.register(r'enrollments', EnrollmentViewSet , basename='enrollments')
router.register(r'add-enrollments', AddEnrollmentViewSet , basename='add-enrollments')
router.register(r'update-users', UserViewSet , basename='update-users')

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view())
]

# adds all of our urls together/custom and rest framework
urlpatterns += router.urls