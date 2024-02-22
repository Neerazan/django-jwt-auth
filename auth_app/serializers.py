from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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



class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={
        'input_type': 'password'
    }, write_only=True)

    new_password = serializers.CharField(max_length=255, style={
        'input_type': 'password'
    }, write_only=True)

    class Meta:
        fields = ['password', 'new_password']



class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    
    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/user/reset'+uid+'/'+token
            print(f"Password Reset Link: {link}")
            return attrs

        else:
            raise serializers.ValidationError('You are not a regisgered user.')
