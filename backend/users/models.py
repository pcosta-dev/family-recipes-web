from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)

    username = models.CharField(max_length=50)
    profile_img = models.ImageField(upload_to="profile_imgs", blank=True, 
                                    null=True)
    birthday = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.username
