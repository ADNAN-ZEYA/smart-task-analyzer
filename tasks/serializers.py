from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Transforms Task objects to/from JSON for API communication.
    """
    
    is_overdue = serializers.SerializerMethodField()
    days_until_deadline = serializers.SerializerMethodField()
    depends_on_titles = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'estimated_duration',
            'complexity',
            'depends_on',
            'depends_on_titles',
            'deadline',
            'created_at',
            'updated_at',
            'started_at',
            'completed_at',
            'assigned_to',
            'tags',
            'is_overdue',
            'days_until_deadline',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_overdue(self, obj):
        """Return whether the task is overdue"""
        return obj.is_overdue
    
    def get_days_until_deadline(self, obj):
        """Return days until deadline"""
        return obj.days_until_deadline
    
    def get_depends_on_titles(self, obj):
        """Return titles of dependent tasks"""
        return {dep.id: dep.title for dep in obj.depends_on.all()}


class TaskListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for task lists.
    Returns essential information only for better performance.
    """
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'priority',
            'deadline',
            'complexity',
            'assigned_to',
        ]
