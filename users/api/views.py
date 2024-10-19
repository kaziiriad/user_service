from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser



from django.contrib.auth.models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kw):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User does not exist"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "success" : True,
                    "username": user.username,
                    "token": token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            reponse = {
                "success" : True,
                "user" : serializer.data,
                "token" : Token.objects.get(user=user).key
            }
            return Response(reponse, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        response = {
            "success": True,
            "detail": "User logged out successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


