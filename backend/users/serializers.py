from .models import CustomUser, Profile
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser class.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the registration requests and create new users.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for the login request with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user

        raise serializers.ValidationError(_("Incorrect credentials"))


class ProfileSerializer(CustomUserSerializer):
    """
    Serializer for the Profile class.
    """

    class Meta:
        model = Profile
        fields = ("birthday", "created_on")


class ProfileImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the profile image from the Profile class.
    """

    class Meta:
        model = Profile
        fields = ("profile_img",)
