from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Smart Task Model - Core data structure for task management.
    
    This model represents a task with intelligent attributes for
    prioritization, dependency tracking, and resource allocation.
    """
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]
    
    # User who owns this task
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    
    # Core Task Information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Task Status & Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    
    # Task Metrics for Smart Algorithms
    estimated_duration = models.FloatField(default=1.0, help_text="Estimated duration in hours")
    complexity = models.IntegerField(default=1, help_text="Complexity score 1-10")
    
    # Dependencies & Scheduling
    depends_on = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents')
    deadline = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Resource Allocation
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    class Meta:
        ordering = ['-priority', 'deadline']
        indexes = [
            models.Index(fields=['user', 'status', 'priority']),
            models.Index(fields=['user', 'deadline']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.deadline and self.status != 'completed':
            return timezone.now() > self.deadline
        return False
    
    @property
    def days_until_deadline(self):
        """Calculate days remaining until deadline"""
        if self.deadline:
            delta = self.deadline - timezone.now()
            return delta.days
        return None
