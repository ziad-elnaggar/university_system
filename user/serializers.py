from rest_framework import serializers
from .models import BaseUser

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id', 'name', 'email', 'hour_rate', 'courses']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['name', 'email', 'password', 'role']

    def create(self, validated_data):
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required fields.")
        return data
