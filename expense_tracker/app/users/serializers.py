from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, authenticate
from expense_tracker.app.users.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['id', 'name', 'email', 'password']
    read_only_fields = ['id']
    extra_kwargs = {
      'password': { 'write_only': True, 'min_length': 4}
    }
   
  def create(self, validated_data):
    return get_user_model().objects.create_user(**validated_data)
  
  
class LoginSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=255, read_only=True)
  email = serializers.EmailField(max_length=255)
  password = serializers.CharField(max_length=255, write_only=True)
  tokens = serializers.CharField(max_length=255, read_only=True)
  
  class Meta:
    model = User
    fields = ['email', 'password', 'name', 'tokens']
    
  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')
    
    user = authenticate(email=email, password=password)
    
    if not user:
      raise AuthenticationFailed('Invalid Credentials')
      
    if not user.is_active:
      raise AuthenticationFailed('Account disabled, contact admin')
      
    if not user.is_verified:
      raise AuthenticationFailed('Email is not verified')
      
    return {
      'email': user.email,
      'name': user.name,
      'tokens': user.tokens(),
    }
  


  