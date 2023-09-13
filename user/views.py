from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, Group
from .serializers import RegistrationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'user_id': user.id,
                'user_name': user.name,
                'user_email': user.email,
                'user_password': user.password
            }
            return Response({'message': f'{user.role.capitalize()} registered successfully', 'data': response_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request, role):
    if request.method == 'POST':
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if not email or not password:
            return Response({'error': 'Both email and password are required fields'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if role != user.role:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }

            return Response({'message': f'{user.role.capitalize()} logged in successfully', 'data': response_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def logout_view(request):
    logout(request)