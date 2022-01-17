from django.urls import path
from .views import ConnectionRequestViewSet, EnrollmentViewSet, ProfileViewSet, current_user, BootcampViewSet, UserList, IndustryViewSet, SkillViewSet, LinkedIn, get_linkedin_id
from rest_framework.routers import DefaultRouter

# create router for views
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'industries', IndustryViewSet, basename='industries')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'bootcamps', BootcampViewSet, basename='bootcamps')
router.register(r'connection-requests', ConnectionRequestViewSet, basename='requests')
router.register(r'enrollments', EnrollmentViewSet , basename='enrollments')

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('linkedin/', LinkedIn),
    path('linkedinSignUp/', get_linkedin_id)
]

# adds all of our urls together/custom and rest framework
urlpatterns += router.urls