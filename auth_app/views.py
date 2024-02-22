from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .serializers import *



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserView(APIView):
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        print(f"This is serializer {serializer}")
        if serializer.is_valid():
            #doing this due to custom model when i try to create user password is not encrypted
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            token = get_tokens_for_user(user=user)
            return Response({
                'token': token,
                'msg': 'User created successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginUserView(APIView):
    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                token = get_tokens_for_user(user=user)
                return Response({
                    'token': token,
                    'msg': 'Login Sucess'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors': {
                        'non_field_errors': ['Email or Password is not valid']
                    }
                }, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data['password']
        new_password = serializer.validated_data['new_password']

        if not authenticate(username=user.username, password=current_password):
            return Response({
                'error': 'Current password is incorrect '
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({
            'msg': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password Reset Link was send, Please check your Email'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)