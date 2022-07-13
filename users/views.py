from django.shortcuts import redirect, render
from users.models import User, Team
from rest_framework.views import APIView
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, TeamCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    
    def get(self, request):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    
    def get(self, request):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                data['email'] = user.email
                data['username'] = user.username
                token = Token.objects.get(user=user).key
                data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response({'success': True}, status=status.HTTP_200_OK)
    
    
class TeamCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TeamCreateSerializer
    
    def get(self, request):
        serializer = self.serializer_class()
        if request.user.is_team_member or request.user.is_team_leader:
            return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
        team_leaders = list(User.objects.filter(is_team_leader=True))
        team_members = list(User.objects.filter(is_team_member=True))
        context = {
            "data format": serializer.data,
            "message": "select from below ids",
            "team_leaders": [member.id for member in team_leaders],
            "team_members": [member.id for member in team_members]
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.is_team_member or request.user.is_team_leader:
            return Response({"errors": "you are unauthorized to change this Task"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        