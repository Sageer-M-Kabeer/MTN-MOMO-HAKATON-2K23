from django.urls import path
from .views import LoginView,RegisterUserView,ValidateOTP

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/',RegisterUserView.as_view()),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),

]