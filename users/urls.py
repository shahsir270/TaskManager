from django.urls import path
from users.views import UserRegistrationView,UserLoginView,UserLogoutView, TeamCreateView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', csrf_exempt(UserRegistrationView.as_view())),
    path('login/', csrf_exempt(UserLoginView.as_view())),
    path('logout/', UserLogoutView.as_view()),
    path('create/team/', csrf_exempt(TeamCreateView.as_view())),
]