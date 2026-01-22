from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from .serializers import DepartmentUserRegistrationSerializer, UserSerializer
from .models import User


# ---------------- JWT TOKEN CUSTOMIZATION ----------------
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 1. ENCRYPT ROLE INTO TOKEN
        # This allows Angular to read the role even after a page refresh
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # 2. RETURN ROLE IN LOGIN RESPONSE
        # This allows Angular to update the UI immediately upon login
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data


# ---------------- LOGIN ----------------
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


# ---------------- REGISTRATION (PUBLIC) ----------------
class RegistrationView(generics.CreateAPIView):
    serializer_class = DepartmentUserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # 🔥 DISABLE JWT AUTH FOR REGISTER

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "username": user.username,
            "role": user.role,
        }, status=status.HTTP_201_CREATED)


# ---------------- LIST USERS (PROTECTED) ----------------
class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---------------- UPDATE USER (PROTECTED) ----------------
class UpdateUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


# ---------------- GET DEPARTMENTS (PUBLIC) ----------------
@api_view(['GET'])
@authentication_classes([])  # 🔥 DISABLE AUTH COMPLETELY
@permission_classes([AllowAny])
def get_departments(request):
    departments = [
        choice[0]
        for choice in User.DEPARTMENT_CHOICES
        if choice[0]
    ]
    return Response(departments)


# ---------------- GET DOMAINS (PUBLIC) ----------------
@api_view(['GET'])
@authentication_classes([])  # 🔥 DISABLE AUTH COMPLETELY
@permission_classes([AllowAny])
def get_domains(request):
    domains = [
        {"value": choice[0], "display": choice[1]}
        for choice in User.DOMAIN_CHOICES
    ]
    return Response(domains)
