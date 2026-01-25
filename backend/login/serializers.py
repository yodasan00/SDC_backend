from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import Department, Domain

User = get_user_model()

# ======================================================
# REGISTRATION SERIALIZER
# ======================================================
class DepartmentUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'phone_number',
            'role',
            'department_name',
            'domain'
        ]

    def validate(self, data):
        role = data.get('role')
        department = data.get('department_name')
        domain = data.get('domain')

        # ---------------- ROLE VALIDATION ----------------
        if role not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError({
                "role": "Invalid role selected."
            })

        # ---------------- DEPARTMENT USER ----------------
        if role == 'DEPARTMENT':
            if department is None:
                raise serializers.ValidationError({
                    "department_name": "Department is required for Department User."
                })
            if not isinstance(department, Department):
                raise serializers.ValidationError({
                    "department_name": "Invalid department selected."
                })

        # ---------------- SDC STAFF ----------------
        elif role == 'SDC':
            if domain is None:
                raise serializers.ValidationError({
                    "domain": "Domain is required for SDC Staff."
                })
            if not isinstance(domain, Domain):
                raise serializers.ValidationError({
                    "domain": "Invalid domain selected."
                })

        # ---------------- OTHER ROLES ----------------
        else:
            data['department_name'] = None
            data['domain'] = None

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ======================================================
# LOGIN SERIALIZER (USERNAME / EMAIL / PHONE)
# ======================================================
# serializers.py (Keep your imports and Registration Serializer as they are)

# ... existing imports ...

# ======================================================
# LOGIN SERIALIZER (USERNAME / EMAIL / PHONE)
# ======================================================
class CustomTokenSerializer(TokenObtainPairSerializer):
    
    # 1. ADD THIS METHOD (moved from views.py)
    # This ensures the 'role' is inside the encoded JWT token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        identifier = attrs.get("username") 
        password = attrs.get("password")
        try:
            user = User.objects.get(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier) |
                Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials")

        data = super().validate({
            "username": user.username, 
            "password": password
        })
        data["username"] = user.username
        data["role"] = user.role
        return data

# ======================================================
# USER LIST / DETAIL SERIALIZER
# ======================================================
class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(
        source='get_role_display',
        read_only=True
    )

    department_display = serializers.CharField(
        source='department_name.name',
        read_only=True
    )

    domain_display = serializers.CharField(
        source='domain.display',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'role_display',
            'phone_number',
            'department_name',
            'department_display',
            'domain',
            'domain_display',
        ]
