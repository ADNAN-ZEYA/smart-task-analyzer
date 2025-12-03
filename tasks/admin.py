from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'importance', 'estimated_hours')
    filter_horizontal = ('dependencies',) # This makes selecting dependencies easy