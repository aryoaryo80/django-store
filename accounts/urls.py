from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('otp-code/', views.UserOtpCodeView.as_view(), name='user_otp_code'),
    path('resend/', views.ResendView.as_view(), name='resend'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
]
