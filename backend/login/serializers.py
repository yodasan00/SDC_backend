from rest_framework import serializers
from .models import User, Department, Domain


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

    def validate(self, data):
        role = data.get('role')
        department = data.get('department_name')
        domain = data.get('domain')

        if role not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError({
                "role": "Invalid role selected."
            })

        if role == 'DEPARTMENT':
            if not department:
                raise serializers.ValidationError({
                    "department_name": "Department is required for Department User."
                })
            if not Department.objects.filter(id=department.id).exists():
                raise serializers.ValidationError({
                    "department_name": "Invalid department selected."
                })

        if role == 'SDC':
            if not domain:
                raise serializers.ValidationError({
                    "domain": "Domain is required for SDC Staff."
                })
            if not Domain.objects.filter(id=domain.id).exists():
                raise serializers.ValidationError({
                    "domain": "Invalid domain selected."
                })

        if role not in ['DEPARTMENT', 'SDC']:
            data['department_name'] = None
            data['domain'] = None

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number'),
            department_name=validated_data.get('department_name'),
            domain=validated_data.get('domain')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
