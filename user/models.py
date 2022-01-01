import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


USER_TYPES = (
    ("normal user", "Normal User"),
    ("business user", "Business User"),
    ("admin", "Admin"),
)

GENDERS = (
    (1, "Male"),
    (2, "Female"),
    (3, "Other"),
)


class UserManager(BaseUserManager):
    """Manager for user model"""
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user with email and password"""
        if not email:
            raise ValueError(_("Email is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with email and password"""
        user = self.create_user(email, password, **extra_fields)
        user.user_type = "admin"
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for the project"""
    email = models.EmailField(_("Email address"), max_length=255, unique=True)
    first_name = models.CharField(max_length=128, default="")
    last_name = models.CharField(max_length=128, default="")
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default="1")
    joined_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """returns string representation of user"""
        full_name = self.get_full_name()
        if full_name and len(full_name) > 1:
            return f"{full_name}"
        else:
            return f"{self.email}"

    def has_perm(self, perm, obj=None):
        """returns true if a user has permission"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """returns True if a user is a staff member"""
        return self.is_superuser

    def get_full_name(self):
        """returns full name of the user"""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """returns first name of the user"""
        return f"{self.first_name}"


class Customer(models.Model):
    """model to manage customer objects in DB"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(_("Full name"), max_length=255, default="")
    display_name = models.CharField(_("Display name"), max_length=128, default="")
    gender = models.CharField(max_length=10, choices=GENDERS, default=2)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    updated_on = models.DateTimeField()
    created_by = models.CharField(max_length=128, default="self")
    updated_by = models.CharField(max_length=128, default="self")

    def __str__(self):
        """returns string representation of customer"""
        full_name = self.get_full_name()
        short_name = self.get_display_name()
        if full_name:
            return f"{full_name}"
        elif short_name:
            return f"{short_name}"
        else:
            return f"{self.phone}"

    def get_full_name(self):
        """returns full name of the customer"""
        return f"{self.full_name}"

    def get_display_name(self):
        """returns short name of the user"""
        return f"{self.display_name}"

    def get_phone_number(self):
        """returns phone number of customer"""
        return f"{self.phone}"
