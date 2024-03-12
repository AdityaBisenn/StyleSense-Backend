# myproject/myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView

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

# myproject/myapp/views.py (continued)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def protected_route(request):
    return Response({'message': 'This is a protected route'}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db import connection
# import os

# import time

# from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# class Test(APIView):
#     def get(self, request):
#         # Check PostgreSQL connection
#         try:
#             # Use a simple query to test the connection
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT 1")
#                 row = cursor.fetchone()
#                 if row:
#                     connected = True
#                 else:
#                     connected = False
#         except Exception as e:
#             connected = False

#         if connected:
#             message = 'PostgreSQL server is connected.'
#         else:
#             message = 'Failed to connect to PostgreSQL server.'

#         return Response({'message': message})

#     def post(self, request):
#         chrome_options = Options()
#         chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--headless") 
#         chrome_options.add_argument("--disable-dev-shm-usage")

#         driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#         url = request.data.get('url')
#         driver.get(url)
#         # print(driver.page_source)
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         # print(soup.prettify())

#         # # save the page source to a file
#         # with open("ajio.html", "w", encoding="utf-8") as file:
#         #     file.write(soup.prettify())

#         # close the webdriver
#         driver.quit()
#         # return the soup as a response
#         return Response(soup.prettify())



# # views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# from rest_framework_jwt.settings import api_settings

# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#                 jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)
#                 return Response({'token': token}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # views.py
# from rest_framework.permissions import IsAuthenticated

# class LogoutAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         # Perform logout operations if any
#         return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)




