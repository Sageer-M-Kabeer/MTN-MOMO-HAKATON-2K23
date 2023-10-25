from django.urls import path
from .views import LoginView,RegisterUserView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/',RegisterUserView.as_view()),
]