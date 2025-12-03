from django.test import TestCase
from datetime import date, timedelta
from .models import Task
from .engine import SmartScoringEngine

class AlgorithmTests(TestCase):
    def test_urgency_weight(self):
        """Urgent tasks should outscore distant ones"""
        t1 = Task.objects.create(title="Urgent", due_date=date.today(), estimated_hours=1, importance=5)
        t2 = Task.objects.create(title="Later", due_date=date.today()+timedelta(days=10), estimated_hours=1, importance=5)
        self.assertTrue(SmartScoringEngine.calculate_score(t1) > SmartScoringEngine.calculate_score(t2))

    def test_dependency_bonus(self):
        """Blocking tasks should get a bonus"""
        blocker = Task.objects.create(title="Blocker", due_date=date.today(), estimated_hours=1, importance=5)
        dependent = Task.objects.create(title="Dependent", due_date=date.today(), estimated_hours=1, importance=5)
        blocker.blocking.add(dependent)
        
        # Blocker should have higher score than a standalone task
        standalone = Task.objects.create(title="Solo", due_date=date.today(), estimated_hours=1, importance=5)
        self.assertTrue(SmartScoringEngine.calculate_score(blocker) > SmartScoringEngine.calculate_score(standalone))

    def test_quick_win(self):
        """Short tasks should outscore long tasks (all else equal)"""
        short = Task.objects.create(title="Short", due_date=date.today(), estimated_hours=1, importance=5)
        long_task = Task.objects.create(title="Long", due_date=date.today(), estimated_hours=10, importance=5)
        self.assertTrue(SmartScoringEngine.calculate_score(short) > SmartScoringEngine.calculate_score(long_task))