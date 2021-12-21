from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


USER_TYPES = (
    ("normal user", "Normal User"),
    ("business user", "Business User"),
    ("admin", "Admin"),
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
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default="1")
    joined_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """returns string representation of user"""
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


# class UserProfile(models.Model):
#     """user details model"""
#     first_name = models.CharField(max_length=64)
#     last_name = models.CharField(max_length=64, null=True, blank=True)
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         """returns string representation of user profile"""
#         return self.get_full_name()
#
#     def get_full_name(self):
#         """returns full name of user"""
#         return f"{self.first_name} {self.last_name}"
#
#     def get_short_name(self):
#         """returns first name of user"""
#         return f"{self.first_name}"

