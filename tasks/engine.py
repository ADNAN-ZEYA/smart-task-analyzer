"""
Smart Task Engine - The Brain of the Smart Task Manager

This module contains the proprietary algorithm that intelligently
analyzes tasks and provides optimal prioritization and recommendations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


class SmartTaskEngine:
    """
    The core engine for intelligent task analysis and prioritization.
    
    This engine analyzes multiple factors including:
    - Task priority and deadline urgency
    - Task dependencies and blocking relationships
    - Complexity and estimated duration
    - Resource allocation and workload balance
    - Historical performance data
    """
    
    def __init__(self, tasks):
        """
        Initialize the engine with a list of tasks.
        
        Args:
            tasks: QuerySet or list of Task objects
        """
        self.tasks = list(tasks)
        self.task_scores = {}
        self._calculate_all_scores()
    
    def _calculate_all_scores(self):
        """Calculate priority scores for all tasks"""
        for task in self.tasks:
            self.task_scores[task.id] = self._calculate_task_score(task)
    
    def _calculate_task_score(self, task) -> float:
        """
        Calculate a comprehensive score for a task.
        
        Score factors:
        1. Priority weight (40%)
        2. Deadline urgency (35%)
        3. Complexity & duration ratio (15%)
        4. Dependencies factor (10%)
        
        Args:
            task: Task object
            
        Returns:
            float: Calculated score (higher = more urgent)
        """
        score = 0
        
        # 1. Priority Weight (40%)
        priority_score = (task.priority / 4) * 40
        score += priority_score
        
        # 2. Deadline Urgency (35%)
        deadline_score = self._calculate_deadline_urgency(task) * 35
        score += deadline_score
        
        # 3. Complexity & Duration Ratio (15%)
        complexity_score = self._calculate_complexity_score(task) * 15
        score += complexity_score
        
        # 4. Dependencies Factor (10%)
        dependency_score = self._calculate_dependency_impact(task) * 10
        score += dependency_score
        
        # Status modifier
        if task.status == 'blocked':
            score *= 0.5  # Reduce score for blocked tasks
        elif task.status == 'completed':
            score = 0  # Completed tasks have no score
        
        return score
    
    def _calculate_deadline_urgency(self, task) -> float:
        """
        Calculate urgency based on deadline.
        
        Returns float 0-1 where 1 is most urgent.
        """
        if not task.deadline:
            return 0.3  # Low urgency if no deadline
        
        now = datetime.now(task.deadline.tzinfo) if task.deadline.tzinfo else datetime.now()
        days_left = (task.deadline - now).days
        
        if days_left < 0:
            return 1.0  # Overdue
        elif days_left == 0:
            return 0.95  # Due today
        elif days_left <= 3:
            return 0.8  # Due soon
        elif days_left <= 7:
            return 0.6  # Due in a week
        elif days_left <= 30:
            return 0.3
        else:
            return 0.1
    
    def _calculate_complexity_score(self, task) -> float:
        """
        Calculate complexity score based on complexity and duration.
        
        Higher complexity and longer duration = higher score.
        """
        # Normalize complexity (1-10) to 0-1
        complexity_factor = task.complexity / 10
        
        # Normalize duration (in hours) - consider >8 hours as high
        duration_factor = min(task.estimated_duration / 8, 1.0)
        
        # Weight them: prefer shorter, simpler tasks for immediate action
        # but also consider that long complex tasks should be started early
        score = (complexity_factor * 0.6 + duration_factor * 0.4)
        
        return score
    
    def _calculate_dependency_impact(self, task) -> float:
        """
        Calculate impact of dependencies.
        
        Tasks that block others should have higher scores.
        Tasks that are blocked should have lower scores.
        """
        blocking_count = task.dependents.count()
        blocked_by_count = task.depends_on.count()
        
        if task.status == 'completed':
            return 0
        
        # Penalize blocked tasks, reward blocking tasks
        impact = (blocking_count * 0.2) - (blocked_by_count * 0.15)
        
        # Normalize to 0-1
        impact = max(0, min(impact, 1))
        return impact
    
    def get_optimized_order(self) -> List:
        """
        Get tasks in optimized order for execution.
        
        Returns:
            List of Task objects sorted by calculated scores
        """
        # Filter out completed tasks
        active_tasks = [t for t in self.tasks if t.status != 'completed']
        
        # Sort by score (descending) and then by ID for stability
        sorted_tasks = sorted(
            active_tasks,
            key=lambda t: (-self.task_scores.get(t.id, 0), t.id)
        )
        
        return sorted_tasks
    
    def analyze_tasks(self) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of all tasks.
        
        Returns:
            Dictionary containing various analytics
        """
        active_tasks = [t for t in self.tasks if t.status != 'completed']
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t.status == 'completed')
        in_progress_tasks = sum(1 for t in active_tasks if t.status == 'in_progress')
        blocked_tasks = sum(1 for t in active_tasks if t.status == 'blocked')
        
        # Calculate total workload
        total_hours = sum(t.estimated_duration for t in active_tasks)
        total_complexity = sum(t.complexity for t in active_tasks)
        
        # Find critical path
        critical_tasks = [t for t in active_tasks if t.priority == 4]
        
        # Find overdue tasks
        overdue_tasks = [t for t in active_tasks if t.is_overdue]
        
        analysis = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'active_tasks': len(active_tasks),
            'in_progress': in_progress_tasks,
            'blocked_tasks': blocked_tasks,
            'overdue_tasks': len(overdue_tasks),
            'total_estimated_hours': round(total_hours, 2),
            'average_complexity': round(total_complexity / len(active_tasks), 2) if active_tasks else 0,
            'critical_tasks': len(critical_tasks),
        }
        
        return analysis
    
    def get_recommendations(self) -> List[str]:
        """
        Generate actionable recommendations based on analysis.
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        analysis = self.analyze_tasks()
        
        # Check for overdue tasks
        if analysis['overdue_tasks'] > 0:
            recommendations.append(
                f"⚠️ URGENT: You have {analysis['overdue_tasks']} overdue task(s). Address these immediately."
            )
        
        # Check for high complexity tasks
        if analysis['average_complexity'] > 7:
            recommendations.append(
                f"💡 High complexity workload detected (avg: {analysis['average_complexity']}/10). "
                "Consider breaking tasks into smaller subtasks."
            )
        
        # Check workload
        if analysis['total_estimated_hours'] > 40:
            recommendations.append(
                f"📊 High workload detected ({analysis['total_estimated_hours']} hours). "
                "Consider prioritizing or delegating tasks."
            )
        
        # Check for blocked tasks
        if analysis['blocked_tasks'] > 0:
            recommendations.append(
                f"🔒 {analysis['blocked_tasks']} task(s) are blocked. "
                "Resolve dependencies to unblock progress."
            )
        
        # Check progress
        if analysis['completion_rate'] < 30 and analysis['active_tasks'] > 0:
            recommendations.append(
                f"🚀 Low completion rate ({analysis['completion_rate']:.0f}%). "
                "Focus on completing in-progress tasks."
            )
        
        # If no issues found
        if not recommendations:
            recommendations.append(
                "✅ Great job! Your task management looks balanced. Keep up the good work!"
            )
        
        return recommendations
