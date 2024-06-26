from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User
from .utils import Util


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
            link = 'http://127.0.0.1:8000/user/reset/' + uid + '/' + token +'/'
            print(f"Password Reset Link: {link}")

            # Send Email
            body = f"Click following link to reset you password {link}"

            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }

            Util.send_email(data=data)
            return attrs

        else:
            raise serializers.ValidationError('You are not a regisgered user.')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=255, 
                                    style={
                                        'input_type': 'password'
                                        }
                                    )
    
    class Meta:
        fields = ['password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uid = self.context.get('uid')
            token = self.context.get('token')

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not valid or Expired')