
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import Team

@shared_task(bind=True)
def send_mail_func(self, id):
    team = Team.objects.get(id=id)
    user = team.team_leader
    mail_subject = "Task Created"
    message = f"hii {user.username} user is created new Task and assigned to your team"
    to_email = user.email
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "send"