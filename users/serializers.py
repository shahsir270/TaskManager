from rest_framework import serializers
from users.models import User, Team

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    class Meta:
        model = User
        fields = ['email','password']
        

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
        
class TeamDetailsSerializer(serializers.ModelSerializer):
    team_leader = UserDetailsSerializer()
    team_members = UserDetailsSerializer(many=True)    
    class Meta:
        model = Team
        fields = '__all__'
        