from django.urls import path
from .views import TaskAnalyzeView, TaskCreateView

urlpatterns = [
    path('analyze/', TaskAnalyzeView.as_view()),
    path('create/', TaskCreateView.as_view()),
]