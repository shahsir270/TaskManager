from django.shortcuts import render
from rest_framework.views import APIView
from task.serializers import TaskCreateSerializer, TaskDetailsSerializer, TaskListSerializer, TaskUpdateSerializer, TaskListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from task.models import Task
from users.models import User,Team
from task.tasks import send_mail_func


# Create your views here.
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = TaskCreateSerializer
    
    def get(self, request, *args, **kwargs):
        if request.user.is_team_member or request.user.is_team_leader:
            return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
        teams = list(Team.objects.all())
        serializer = self.serializer_class()
        team_ids = [team.id for team in teams]
        context = {
            "data format": serializer.data,
            "message": "select team from below ids",
            "teams": team_ids
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        if request.user.is_team_member or request.user.is_team_leader:
            return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            team = serializer.data.get('team')
            send_mail_func.delay(team)
            data = TaskDetailsSerializer(task).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer
    
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = self.serializer_class(task)
        status_choices = ('In progress','Under Review','Done')
        members = list(i.id for i in task.team.team_members.all())
        if task.team.team_leader.id == request.user.id:
            context = {
                "task fields" : serializer.data,
                "conditions" : "select team member ids from given below members",
                "members" : members,
                "status choices": status_choices
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, pk):
        given_members = request.data.get('team_members')
        task = Task.objects.get(pk=pk)
        serializer = self.serializer_class(task, data=request.data)
        team_members = list(task.team.team_members.all())
        team_members_list = []
        if task.team.team_leader.id == request.user.id:
            if serializer.is_valid():
                for member_id in given_members:
                    team_members_list.append(User.objects.get(id=member_id))
                for member in team_members_list:
                    if member not in team_members:
                        return Response({"errors": "team members are not in allocated team"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)

class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        task = Task.objects.filter(pk=pk)
        status_choices = ('In progress','Under Review','Done')
        team_members_list = [member.id for member in task.first().team_members.all()]
        if request.user.id in team_members_list:
            context = {"status":task.first().status, "select choices":status_choices}
            return Response(context, status=status.HTTP_200_OK)
        return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request, pk):
        task = Task.objects.filter(pk=pk)
        task_status = request.data.get('status')
        team_members_list = [member.id for member in task.first().team_members.all()]
        if request.user.id in team_members_list:
            task.update(status=task_status)
            return Response({"message":"status updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
    

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer
    
    def get(self, request):
        tasks = Task.objects.all()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        