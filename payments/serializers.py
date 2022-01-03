from rest_framework import serializers

from payments.models import Payment
from orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    """serializes payment objects"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        """creates a new payment obj with validated data"""
        order_id = validated_data["order"]
        order = Order.objects.filter(pk=order_id).first()
        if not order:
            error = {
                "message": f"Order with id ({order_id}) is not found"
            }
            raise serializers.ValidationError()

        request_user = validated_data.pop("request_user")
        validated_data[""]
