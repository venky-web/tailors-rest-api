from datetime import datetime

from rest_framework import serializers

from orders import models


def update_order(user, order):
    """
        Updates order updated_by, updated_on columns
        Args: User, Order
    """
    order.updated_by = user.id
    order.updated_on = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    order.save()


class OrderSerializer(serializers.ModelSerializer):
    """serializes order model objects"""
    created_by = serializers.CharField(required=False)
    updated_by = serializers.CharField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    class Meta:
        model = models.Order
        fields = "__all__"
        read_only_fields = ("id", "created_by", "updated_by", "updated_on", "created_on")

    def create(self, validated_data):
        """Creates a new order object in db"""
        validated_data["updated_on"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            user = validated_data.pop("user")
        validated_data["created_by"] = user.id
        validated_data["updated_by"] = user.id
        order = models.Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        """updates an order object with validated data"""
        instance.customer_id = validated_data.get("'customer_id", instance.customer_id)
        instance.total_amount = validated_data.get("total_amount", instance.total_amount)
        instance.delivery_date = validated_data.get("delivery_date", instance.delivery_date)
        instance.order_status = validated_data.get("order_status", instance.order_status)
        instance.comments = validated_data.get("comments", instance.comments)
        instance.is_one_time_delivery = validated_data.get("is_one_time_delivery",
                                                           instance.is_one_time_delivery)
        instance.updated_on = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            user = validated_data.pop("user")
        instance.updated_by = user.id
        instance.save()
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    """serializes order item objects"""
    class Meta:
        model = models.OrderItem
        fields = "__all__"
        read_only_fields = ("id", "created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        """creates a new order item in db"""
        order = validated_data.pop("order")
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")

        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        validated_data["created_by"] = request_user.id
        validated_data["updated_by"] = request_user.id
        validated_data["updated_on"] = now
        print(validated_data)
        validated_data["order_id"] = order
        order_item = models.OrderItem.objects.create(**validated_data)
        update_order(request_user, order)

        return order_item

    def update(self, instance, validated_data):
        """updates an order item in db and order items list"""
        order = validated_data["order"]
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")

        for key in instance:
            instance[key] = validated_data.get(key, instance[key])

        instance.updated_by = request_user.id
        instance.updated_on = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        instance.save()
        update_order(request_user, order)

        return instance