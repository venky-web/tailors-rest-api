from rest_framework import serializers

from products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """serializes a product image model obj"""
    # created_by = serializers.CharField(required=False)
    # updated_by = serializers.CharField(required=False)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ("id", "image_url", "image")
        read_only_fields = ("id",)
        extra_kwargs = {
            "image": {"write_only": True}
        }

    def get_image_url(self, instance):
        """returns absolute url of image"""
        request = self.context.get("request")
        if hasattr(instance, "image"):
            image_url = instance.image.url
            return request.build_absolute_uri(image_url)

        return None

    def create(self, validated_data):
        """creates a new image details obj in DB"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_user = request.user
            validated_data.pop("request_user")
        else:
            request_user = validated_data.pop("request_user")

        print(validated_data)
        validated_data["created_by"] = request_user.id
        validated_data["updated_by"] = request_user.id
        product_image = ProductImage.objects.create(**validated_data)
        return product_image


class ProductSerializer(serializers.ModelSerializer):
    """serializes product objects"""
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    class Meta:
        model = Product
        fields = (
            "id", "name", "product_code", "price", "cost", "is_service", "created_on", "updated_on",
            "created_by", "updated_by", "is_deleted", "is_available"
        )
        read_only_fields = ("id", "created_by", "updated_by")

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
        instance.save(using=self._db)
        return instance
