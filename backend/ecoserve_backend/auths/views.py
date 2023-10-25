from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from users.models import User
from .serializers import UserLoginSerializer, UserSerializer
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from .backends import EmailPhoneUsernameAuthenticationBackend as EoP


class RegisterUserView(GenericAPIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    '''Login api view That authenticate users with email or phone number
    and password'''
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny,]

    def post(self,request):
        data = request.data
        phone_number = data.get('phone_number')
        password = data.get('password')
        email = data.get('email')

         # Attempt to authenticate with either email or phone number
        user = None
        if email:
            user = EoP.authenticate(request, username=email, password=password)
        elif phone_number:
            user = EoP.authenticate(request, username=phone_number, password=password)
        
        if user:
            expiration_time = datetime.utcnow() + timedelta(days=1)
            payload = {
                'phone_number': str(user.phone_number),
                'exp': expiration_time  # Add 24hrs expiration to the token 
            }
            auth_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

            serializer = UserLoginSerializer(user)

            data = {
                'user':serializer.data, 'token':auth_token
            }
            return Response(data,status=status.HTTP_200_OK)
        
        return Response({'detail':'Invalid Credentials.'},status=status.HTTP_400_BAD_REQUEST)