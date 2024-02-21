from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # extra_kwargs={
        #     'password': {'write_only': True}
        # }


class UserLoginSerializer(serializers.Serializer):
    # print(f"This is serirlizers {password}, {username}")
    username = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    id = serializers.IntegerField()