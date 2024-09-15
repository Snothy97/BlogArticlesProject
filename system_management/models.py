from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
import system_management.constants as constants

class UserType(models.Model):
    """A model that represents a user type e.g. ADMIN."""

    name = models.CharField(max_length=50)

    class Meta:
        """Metaclass for user types"""
        verbose_name = "User Type"
        verbose_name_plural = "User Types"

    def __str__(self):
        return str(self.name)

class UserManager(BaseUserManager):
    """
    Django user management class.
    """

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a User with the given email and password.

        :param self:
            Class self object.
        :param email:
            Email field for user object.
        :param password:
            Password field for user object.
        :param first_name:
            First name field for user object.
        :param last_name:
            Last name field for user object.
        :param extra_fields:
            Any additional fields to be added to the user object.
        :return:
            created user object.

        """

        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', first_name)
        extra_fields.setdefault('last_name', last_name)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        :param self:
            Class self object.
        :param email:
            Email field for user object.
        :param password:
            password field for user object.
        :param extra_fields:
            Any additional fields to be added to the user object.
        :return:
            created user object from create user function.
        """

        try:
            user_type_id = UserType.objects.get(name=constants.ADMIN).id

        except ObjectDoesNotExist:
            raise ValueError(_(f'{constants.ADMIN} role not found'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type_id', user_type_id)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password, **extra_fields)
          
        return user



class User(AbstractUser):
    """A model that represents a user of the application."""

    username = None
    email = models.EmailField(max_length=255, unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    

    # Foreign key(s) to the user model
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for user class"""
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """String representation of the user object."""
        return f"{self.email}"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.

        :return:
            Full name of the user.
        """
        return f"{self.first_name} {self.last_name}"



class Profile(models.Model):
    """A model for the user profile containing additional user information."""

    id_number = models.CharField(max_length=13,null=True,blank=True )
    passport_number = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=10)
    street_address = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    postal_code = models.CharField(max_length=5, default="")
    first_login = models.BooleanField(default=False)
    lockout_start_time = models.DateTimeField(null=True)

    # Foreign key(s) to the profile model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    class Meta:
        """Metaclass for user profile class"""
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user}'s profile"

class Province(models.Model):
        name = models.CharField(max_length=255)