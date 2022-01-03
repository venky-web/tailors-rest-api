from django.db import models
from django.conf import settings

from orders.models import Order


class Payment(models.Model):
    """payment model in db"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name="payments", related_query_name="payment")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments",
                              related_query_name="payment")
    paid_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    payment_date = models.DateTimeField()
    mode_of_payment = models.CharField(max_length=50, default="cash")
    created_by = models.CharField(max_length=255, default="")

    class Meta:
        ordering = ("-payment_date",)

    def __str__(self):
        """string representation of payment"""
        return f"{self.id} - {self.paid_amount}"

