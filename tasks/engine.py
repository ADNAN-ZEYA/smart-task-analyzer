from datetime import date
import math

class SmartScoringEngine:
    @staticmethod
    def calculate_score(task):
        today = date.today()
        
        # 1. URGENCY (Exponential Decay)
        days_until = (task.due_date - today).days
        if days_until < 0: urgency = 50 
        elif days_until == 0: urgency = 40
        else: urgency = 30 / (days_until + 1)

        # 2. IMPORTANCE (Weighted)
        imp_score = task.importance * 3.5

        # 3. EFFORT (Quick Wins)
        effort_bonus = 10 / max(task.estimated_hours, 1)

        # 4. DEPENDENCIES (Graph Weight)
        dep_bonus = task.blocking.count() * 5

        return round(urgency + imp_score + effort_bonus + dep_bonus, 2)

    @staticmethod
    def generate_explanation(task, score):
        days = (task.due_date - date.today()).days
        reasons = []
        if days <= 1: reasons.append("Due very soon")
        if task.importance >= 8: reasons.append("High Importance")
        if task.blocking.count() > 0: reasons.append(f"Blocks {task.blocking.count()} tasks")
        if task.estimated_hours < 2: reasons.append("Quick win")
        
        return ", ".join(reasons) if reasons else "Standard priority"