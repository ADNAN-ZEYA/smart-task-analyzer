from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from .auth_views import login, register
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok'})

# Create a router and register the TaskViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('health/', health_check, name='health'),
    path('', include(router.urls)),
    path('auth/login/', login, name='login'),
    path('auth/register/', register, name='register'),
]
