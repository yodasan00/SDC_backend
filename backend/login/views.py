from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from .models import User, Department, Domain
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    DepartmentUserRegistrationSerializer, 
    UserSerializer, 
    CustomTokenSerializer 
)

class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = DepartmentUserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "username": user.username,
            "role": user.role,
        }, status=status.HTTP_201_CREATED)


class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_departments(request):
    departments = Department.objects.all()
    return Response([
        {
            "id": d.id,
            "name": d.name
        }
        for d in departments
    ])


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_domains(request):
    domains = Domain.objects.all()
    return Response([
        {
            "id": d.id,
            "value": d.value,
            "display": d.display
        }
        for d in domains
    ])
