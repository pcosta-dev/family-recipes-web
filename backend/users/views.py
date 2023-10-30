from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import (
    CustomUserSerializer,
    ProfileImageSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class UserRegisterationAPIView(GenericAPIView):
    """
    Endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {
                "refresh": str(token),
                "access": str(token.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"error": "User with this email already exists."},
                status=status.HTTP_409_CONFLICT,
            )


class UserLoginAPIView(GenericAPIView):
    """
    Endpoint to authenticate existing users with their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            serializer = CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {
                "refresh": str(token),
                "access": str(token.access_token),
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(
                {"error": "Incorrect credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserLogoutAPIView(GenericAPIView):
    """
    Endpoint to logout.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except NotFound:
            return Response(
                {"error": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAPIView(RetrieveUpdateAPIView):
    """
    Get and update user information.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get and update user's profile.
    """

    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileImageAPIView(RetrieveUpdateAPIView):
    """
    Get and update user's profile image.
    """

    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileImageSerializer

    def get_object(self):
        return self.request.user.profile
