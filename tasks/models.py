from django.db import models
from django.core.exceptions import ValidationError

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    estimated_hours = models.IntegerField(help_text="Time in hours")
    importance = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    completed = models.BooleanField(default=False)
    # Self-referencing ManyToMany for dependencies
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocking')

    def clean(self):
        # Prevent task from waiting on itself
        if self.pk and self in self.dependencies.all():
            raise ValidationError("A task cannot depend on itself.")

    def __str__(self):
        return self.title