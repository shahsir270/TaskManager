from rest_framework import serializers
from task.models import Task
from users.models import Team
from users.serializers import TeamCreateSerializer, TeamDetailsSerializer, UserDetailsSerializer

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'team')
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('team_members','status', 'started_at', 'completed_at')


class TaskDetailsSerializer(serializers.ModelSerializer):
    team = TeamDetailsSerializer()
    
    class Meta:
        model = Task
        fields = ('name', 'team')


class TaskListSerializer(serializers.ModelSerializer):
    team = TeamDetailsSerializer()
    team_members = UserDetailsSerializer(many=True)
    class Meta:
        model = Task
        fields = '__all__'
        