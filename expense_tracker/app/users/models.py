from django.db import models
from django.contrib.auth.models import (
  BaseUserManager,
  PermissionsMixin,
  AbstractBaseUser
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('Email is required')
    
    if not password:
      raise ValueError('Password is required')
    
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, password):
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user

class User(AbstractBaseUser, PermissionsMixin):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  is_verified = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  
  def __str__(self):
    return self.email
  
  def tokens(self):
    refresh = RefreshToken.for_user(user=self)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token)
    }
