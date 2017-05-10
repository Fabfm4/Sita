import os
from hashlib import md5

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone

class UserManager(BaseUserManager):
    """Custom Manager for crete users"""

    def _create_user(self, email, password, **extra_fields):
        """ Create new Users. """

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login = timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a user."""

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

def get_user_image_path(instance, filename):
    """
    Get the upload path to the profile image.
    """
    return '{0}/{1}{2}'.format(
        "users/originals",
        md5(filename).hexdigest(),
        os.path.splitext(filename)[-1]
    )

class User(AbstractBaseUser, PermissionsMixin):
    """Create custom model User."""

    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    activation_code = models.CharField(max_length=254)
    reset_pass_code = models.CharField(max_length=254)
    conekta_customer = models.CharField(max_length=254)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    logined_date = models.DateField(null=True)
    has_subscription = models.BooleanField(default=False)

    @property
    def thumbnail_settings(self):
        """
        Property used to configurate thumbnail creation settings.
        """
        return {
            "dimension": "200x200",
            "original_field": "photo",
        }

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return "{0} {1}".format(self.name, self.last_name)

    def get_short_name(self):
        return "{0}".format(self.name)

class Subscription(models.Model):
    """ Create The subscriptions from User."""

    expiration_date = models.DateField()
    is_current = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)
    time_in_minutes = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
