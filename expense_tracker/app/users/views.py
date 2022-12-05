from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import jwt

from expense_tracker.app.users.models import User
from expense_tracker.app.users.serializers import UserSerializer, LoginSerializer
from expense_tracker.util.email import Email

# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
  serializer_class = UserSerializer
  
  def post(self, request, *args, **kwargs):
    try:
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      user_data = serializer.data
      
      user = User.objects.get(email = user_data['email'])
      token = RefreshToken.for_user(user).access_token
      
      current_site = get_current_site(request).domain
      relative_link = reverse('email-verify')
      abs_url = 'http://'+current_site+relative_link+'?token='+str(token)
      email_body = f'Hi {user.email}, Use link below to verify your email\n {abs_url}'
      
      data = { 
              'email_body': email_body,
              'subject': 'Verify your email',
              'to_email': user.email
              }
      Email.send_email(data)
        
      return Response(user_data, status=status.HTTP_201_CREATED)
    except Exception as e:
      raise APIException(str(e))
    
      
    
class VerifyEmailAPIView(generics.GenericAPIView):
  def get(self, request, *args, **kwargs):
    token = request.query_params.get('token')
    try:
      payload = jwt.decode(token, settings.SECRET_KEY)
      user = User.objects.get(id = payload['user_id'])
      if not user.is_verified:
        user.is_verified = True
        user.save()
      return Response({ 'email': 'email has been verified successfully'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as e:
      return Response({ 'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as e:
      return Response({ 'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
  serializer_class = LoginSerializer
  
  def post(self, request):
    try:
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      raise APIException(str(e))
    
    