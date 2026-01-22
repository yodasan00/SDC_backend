from rest_framework import serializers
from .models import User


# ---------------- USER REGISTRATION ----------------
class DepartmentUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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

    # -------- ROLE-AWARE VALIDATION --------
    def validate(self, data):
        role = data.get('role')
        department = data.get('department_name')
        domain = data.get('domain')

        # Validate role choice
        if role not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError({
                "role": "Invalid role selected."
            })

        # Department User must have department
        if role == 'DEPARTMENT':
            if not department:
                raise serializers.ValidationError({
                    "department_name": "Department is required for Department User."
                })
            if department not in dict(User.DEPARTMENT_CHOICES):
                raise serializers.ValidationError({
                    "department_name": "Invalid department selected."
                })

        # SDC Staff must have domain
        if role == 'SDC':
            if not domain:
                raise serializers.ValidationError({
                    "domain": "Domain is required for SDC Staff."
                })
            if domain not in dict(User.DOMAIN_CHOICES):
                raise serializers.ValidationError({
                    "domain": "Invalid domain selected."
                })

        # Other roles: safely default values
        if role not in ['DEPARTMENT', 'SDC']:
            data['department_name'] = ''
            data['domain'] = 'NONE'

        return data

    # -------- CREATE USER --------
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number'),
            department_name=validated_data.get('department_name', ''),
            domain=validated_data.get('domain', 'NONE')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ---------------- USER LIST / VIEW ----------------
class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(
        source='get_role_display',
        read_only=True
    )
    department_display = serializers.CharField(
        source='get_department_name_display',
        read_only=True
    )
    domain_display = serializers.CharField(
        source='get_domain_display',
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
            'department_display',
            'domain',
            'domain_display',
        ]
