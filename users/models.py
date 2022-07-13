from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class User(AbstractUser):
  username = models.CharField(max_length = 50)
  email = models.EmailField('email address', unique = True)
  is_team_leader = models.BooleanField(default=False)
  is_team_member = models.BooleanField(default=False)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  def __str__(self):
      return "{}".format(self.email)


#create tokens for users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

class Team(models.Model):
    name = models.CharField(max_length=64)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_team_leader': True}, related_name="team_leader")
    team_members = models.ManyToManyField(User, limit_choices_to={'is_team_member': True}, related_name="team_member")
    
    def __str__(self):
        return self.name
    