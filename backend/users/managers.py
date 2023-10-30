from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser model where 'email' is used as the unique identifier
    for authentication instead of 'username'.
    """

    def create_user(self, email: str, password: str, **extra_fields: dict):
        """
        Create and save a user with given email and password.
        """
        if not email:
            raise ValueError(_("Email field cannot be empty"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_super_user(self, email: str, password: str, **extra_fields: dict):
        """
        Create and save a superuser with given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True"))

        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)
