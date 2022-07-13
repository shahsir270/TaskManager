from django.conf import UserSettingsHolder
from django.db import models
from users.models import User, Team
from django.core.validators import ValidationError

# Create your models here.

status_choices = (
    ('Assigned','Assigned'),
    ('In progress','In progress'),
    ('Under Review','Under Review'),
    ('Done','Done'), 
)

class Task(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="task_allocated_team")
    team_members = models.ManyToManyField(User, help_text="Task assigned to users")
    status = models.CharField(max_length=16, choices=status_choices, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
    