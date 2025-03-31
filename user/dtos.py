from rest_framework import serializers
from api.models import User
from django.contrib.auth.hashers import make_password

class RegisterRequestDto(serializers.ModelSerializer):
    """DTO for user registration"""
    email = serializers.EmailField(required=True, write_only=True)
    full_name = serializers.CharField(required=True, write_only=True)
    role = serializers.ChoiceField(choices=["customer", "pt", "admin"], default="customer")
    profile_picture = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "role", "profile_picture"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

class RegisterResponseDto(serializers.ModelSerializer):
    """DTO for user registration response"""
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    role = serializers.ChoiceField(choices=["customer", "pt", "admin"], read_only=True)
    profile_picture = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "profile_picture", "created_at"]

class LoginRequestDto(serializers.Serializer):
    """DTO for user login"""
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

class LoginResponseDto(serializers.Serializer):
    """DTO for user login response"""
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    role = serializers.ChoiceField(choices=["customer", "pt", "admin"], read_only=True)
    profile_picture = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)