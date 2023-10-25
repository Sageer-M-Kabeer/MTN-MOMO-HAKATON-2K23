import jwt
from rest_framework import authentication,exceptions
from django.conf import settings
from users.models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model



class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        print(auth_data)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            # payload=jwt.decode(token, settings.JWT_SECRET_KEY)
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

            user = User.objects.get(phone_number = payload['phone_number'])
            return (user,token)


        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid Authorization header format')
            
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid,login')
        
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token has expired,login')

        return super().authenticate(request)

User = get_user_model()

class EmailPhoneUsernameAuthenticationBackend(object):
    @staticmethod
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(phone_number=username) | Q(email=username)
            )

        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    

