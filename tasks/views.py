from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer, TaskListSerializer
from .engine import SmartTaskEngine


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Task management.
    
    Provides CRUD operations and intelligent task analysis.
    Requires authentication via JWT token.
    """
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_to']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['priority', 'deadline', 'created_at', 'complexity']
    ordering = ['-priority', 'deadline']
    
    def get_queryset(self):
        """Return tasks only for the current user"""
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user when creating a task"""
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        """Use simplified serializer for list views"""
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    @action(detail=False, methods=['get'])
    def analyze(self, request):
        """
        Analyze all tasks and return optimized prioritization.
        
        GET /api/tasks/analyze/
        
        Returns:
            - optimized_order: List of tasks in optimal execution order
            - analysis: Detailed analysis from the smart algorithm
            - recommendations: Action items for task management
        """
        tasks = self.get_queryset()
        engine = SmartTaskEngine(tasks)
        
        analysis = engine.analyze_tasks()
        optimized_tasks = engine.get_optimized_order()
        recommendations = engine.get_recommendations()
        
        return Response({
            'optimized_order': TaskSerializer(optimized_tasks, many=True).data,
            'analysis': analysis,
            'recommendations': recommendations,
        })
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        Mark a task as in progress.
        
        POST /api/tasks/{id}/start/
        """
        task = self.get_object()
        from django.utils import timezone
        
        task.status = 'in_progress'
        task.started_at = timezone.now()
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark a task as completed.
        
        POST /api/tasks/{id}/complete/
        """
        task = self.get_object()
        from django.utils import timezone
        
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """
        Mark a task as blocked.
        
        POST /api/tasks/{id}/block/
        """
        task = self.get_object()
        task.status = 'blocked'
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
