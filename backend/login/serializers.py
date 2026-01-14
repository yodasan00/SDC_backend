from rest_framework import serializers
from .models import User

class DepartmentUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role='DEPARTMENT'  # force role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user