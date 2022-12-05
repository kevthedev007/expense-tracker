from django.urls import path
from expense_tracker.app.users.views import (
  RegisterAPIView,
  VerifyEmailAPIView,
  LoginAPIView
)

urlpatterns = [
  path('register/', RegisterAPIView.as_view(), name='register'),
  path('verify-email/', VerifyEmailAPIView.as_view(), name='email-verify'),
  path('login/', LoginAPIView.as_view(), name='login')
]