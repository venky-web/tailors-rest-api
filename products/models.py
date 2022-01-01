from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """model for product and service"""
    name = models.CharField(_("Name"), max_length=255, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    product_code = models.CharField(max_length=10, unique=True)
    is_service = models.BooleanField(default=False)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """returns string representation of product"""
        return f"{self.name}"

    def get_product_code(self):
        """returns product code"""
        return f"{self.product_code}"
