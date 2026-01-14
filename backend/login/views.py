# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.response import Response
# from rest_framework import status, generics
# from .serializers import DepartmentUserRegistrationSerializer

# class CustomTokenSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data['role'] = self.user.role
#         data['username'] = self.user.username
#         return data

# class LoginAPIView(TokenObtainPairView):
#     serializer_class = CustomTokenSerializer

# class RegistrationView(generics.CreateAPIView):
#     serializer_class = DepartmentUserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "message": "Department user registered successfully",
#             "username": user.username,
#             "role": user.role
#         }, status=status.HTTP_201_CREATED)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import DepartmentUserRegistrationSerializer

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

class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = DepartmentUserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Open registration

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Department user registered successfully",
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_201_CREATED)