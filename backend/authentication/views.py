# myproject/myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.http import JsonResponse
import requests
from django.db import connection
import os
from authentication.models import CustomUser
from google.oauth2 import id_token
from google.auth.transport import requests

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serialized_user = UserSerializer(user).data  # Serialize user data
            return Response({
                'user': serialized_user,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

# Helper function to generate JWT token
def generate_jwt_token():
    # Implementation to generate JWT token
    pass

class GoogleTokenExchangeAPIView(APIView):
    permission_classes = []

    def post(self, request):
        # Extract the Google access token from the request data
        token = request.data.get('token')
        print(token)

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        print(userid)

        return JsonResponse({'message': 'Token verified successfully'}, status=status.HTTP_200_OK)
        
        # Make a request to Google's token verification endpoint to verify the token
        # google_response = requests.get(
        #     'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=${token}'
        # )
        # google_data = google_response.json()
        # print(google_response.text)

        # if google_response.status_code == 200 and google_data.get('aud') == settings.GOOGLE_CLIENT_ID:
        #     # Google token is valid, proceed with user login or signup
        #     email = google_data.get('email')
        #     if email:
        #         # Check if user exists with this email
        #         user = CustomUser.objects.filter(email=email).first()
        #         if user is None:
        #             # User doesn't exist, create a new user
        #             user = CustomUser.objects.create_user(email=email)
                
        #         # Authenticate and login the user
        #         user = authenticate(request, email=email)
        #         if user:
        #             login(request, user)
        #             refresh = RefreshToken.for_user(user)
        #             access_token = AccessToken.for_user(user)
        #             serialized_user = UserSerializer(user).data
        #             return Response({
        #                 'user': serialized_user,
        #                 'refresh': str(refresh),
        #                 'access': str(access_token),
        #                 'message': 'User authenticated successfully'
        #             }, status=status.HTTP_200_OK)
        #         else:
        #             return Response({'error': 'Failed to authenticate user'}, status=status.HTTP_401_UNAUTHORIZED)
        #     else:
        #         return Response({'error': 'No email provided in Google response'}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     # Google token is invalid or doesn't match your client ID
        #     return Response({'error': 'Invalid Google access token'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_route(request):
    return Response({'message': 'This is a protected route'}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Test(APIView):
    def get(self, request):
        # Check PostgreSQL connection
        try:
            # Use a simple query to test the connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row:
                    connected = True
                else:
                    connected = False
        except Exception as e:
            connected = False

        if connected:
            message = 'PostgreSQL server is connected.'
        else:
            message = 'Failed to connect to PostgreSQL server.'

        return Response({'message': message})

