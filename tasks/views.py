from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .engine import SmartScoringEngine
from datetime import date

# 1. API to Create New Tasks (This makes the form work)
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# 2. API to Analyze and Sort Tasks
class TaskAnalyzeView(APIView):
    def post(self, request):
        # Fetch uncompleted tasks
        tasks = Task.objects.filter(completed=False)
        strategy = request.data.get('strategy', 'smart_balance')
        
        results = []
        for task in tasks:
            data = TaskSerializer(task).data
            
            # --- STRATEGY LOGIC ---
            if strategy == 'deadline':
                days = (task.due_date - date.today()).days
                # Lower days = higher score (urgent)
                data['score'] = 100 - (days * 2)
                data['explanation'] = f"Due in {days} days"
                
            elif strategy == 'impact':
                # Importance is king
                data['score'] = task.importance * 10
                data['explanation'] = f"Importance Rating: {task.importance}/10"
                
            elif strategy == 'quick_wins':
                # Shortest tasks first
                data['score'] = 100 - (task.estimated_hours * 2)
                data['explanation'] = f"Takes {task.estimated_hours} hours"
                
            else:
                # SMART BALANCE (Your Algorithm)
                data['score'] = SmartScoringEngine.calculate_score(task)
                data['explanation'] = SmartScoringEngine.generate_explanation(task, data['score'])
            
            results.append(data)

        # Sort descending by score
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        return Response(sorted_results)