from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """serializes product objects"""
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by")

    def create(self, validated_data):
        """creates a new product with validated data"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")

        validated_data["created_by"] = request_user.id
        validated_data["updated_by"] = request_user.id
        validated_data["is_available"] = True
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        """updates a product obj"""
        request = self.context.get("user")
        if request and hasattr(request, "user"):
            request_user = request.user
        else:
            request_user = validated_data.pop("request_user")
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.product_code = validated_data.get("product_code", instance.product_code)
        instance.is_service = validated_data.get("is_service", instance.is_service)
        instance.updated_on = validated_data.get("updated_on", instance.updated_on)
        instance.is_deleted = validated_data.get("is_deleted", instance.is_deleted)
        instance.is_available = validated_data.get("is_available", instance.is_available)

        instance.updated_by = request_user.id
        instance.save()
        return instance
