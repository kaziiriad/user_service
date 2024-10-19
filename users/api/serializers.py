from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "Username already exists!",
            }
            raise ValidationError(detail=detail)
        return username
    
    def validate(self, instance):
        if instance['password'] != instance['password_confirmation']:
            detail = {
                "detail": "Passwords do not match!",
            }
            raise ValidationError(detail=detail)
        
        if User.objects.filter(email=instance['email']).exists():
            detail = {
                "detail": "Email already exists!",
            }
            raise ValidationError(detail=detail)
        
        return instance
    
    def create(self, validated_data):
        passwords = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        user = User.objects.create(**validated_data)
        user.set_password(passwords)
        user.save()
        Token.objects.create(user=user)
        return user
