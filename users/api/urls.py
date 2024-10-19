from django.urls import path, include
from . import views

urlpatterns = [

    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    path('register/', views.UserRegisterAPIView.as_view(), name='register')

    
]
