from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from products import serializers
from products.models import Product, ProductImage


def get_current_time():
    """returns current time"""
    now = timezone.now().isoformat()
    return now


def get_product_images(product_id, main_image=False):
    """returns product main image or list of images
        args: product_id, main_image (default=False)
    """
    queryset = ProductImage.objects.filter(product_id=product_id).order_by("-id").only("image")
    if main_image:
        img = queryset.filter(is_main_image=True)
        if img:
            return img
        else:
            try:
                return queryset[:1]
            except:
                return None
    else:
        return queryset


class ProductListCreateView(ListCreateAPIView):
    """list and create view of product"""
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """returns queryset of products"""
        is_deleted = self.request.query_params.get('isDeleted')
        if is_deleted == "true":
            return Product.objects.filter(is_deleted=True).order_by("-id")
        else:
            return Product.objects.filter(is_deleted=False).order_by("-id")

    def list(self, request, *args, **kwargs):
        """returns list of products"""
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        products = []
        for product in serializer.data:
            images = get_product_images(product["id"], True)
            product["images"] = serializers.ProductImageSerializer(
                images,
                many=True,
                context={"request": request}
            ).data
            products.append(product)

        return Response(products, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """creates a new product in the db"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        now = get_current_time()
        serializer.save(request_user=user, created_on=now, updated_on=now)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """Get, update and delete product view"""
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """returns product queryset"""
        products = Product.objects.filter(is_deleted=False)
        return products

    def retrieve(self, request, *args, **kwargs):
        """returns a single product object"""
        product = get_object_or_404(Product, pk=kwargs["id"])
        serializer = self.serializer_class(product)
        response_data = serializer.data
        images = get_product_images(kwargs["id"])
        response_data["images"] = serializers.ProductImageSerializer(
            images,
            many=True,
            context={"request": request}
        ).data
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """updates a product obj"""
        product = get_object_or_404(Product, pk=kwargs["id"])
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        serializer.save(request_user=user, updated_on=get_current_time())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """marks a product is_deleted to true"""
        user = self.request.user
        product = get_object_or_404(Product, pk=kwargs["id"])
        modified_product = self.serializer_class(product).data
        modified_product["is_deleted"] = True
        serializer = self.serializer_class(product, data=modified_product)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(request_user=user, updated_on=get_current_time())
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductImageView(ListCreateAPIView):
    """returns a list or creates a product image"""
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def list(self, request, *args, **kwargs):
        """returns a list of product images"""
        product_id = kwargs["id"]
        images = get_product_images(product_id)
        serializer = serializers.ProductImageSerializer(
            images,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """creates a new product image in server"""
        product_id = kwargs["id"]
        product = get_object_or_404(Product, pk=product_id)
        if not product:
            return Response(f"Product with id {product_id} is not found", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        now = get_current_time()
        serializer.save(product=product, request_user=user, created_on=now, updated_on=now)
        return Response(serializer.data, status=status.HTTP_200_OK)
