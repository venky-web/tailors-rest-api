from django.db import models


class FirebaseUser(models.Model):
    """user model for firebase"""
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=128, null=True, blank=True)
