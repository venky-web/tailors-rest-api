from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products import serializers
from products.models import Product


def get_current_time():
    """returns current time"""
    now = timezone.now().isoformat()
    return now


class ProductListCreateView(ListCreateAPIView):
    """list and create view of product"""
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """returns queryset of products"""
        is_deleted = self.request.query_params.get('isDeleted')
        if is_deleted == "true":
            return Product.objects.filter(is_deleted=True)
        else:
            return Product.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        """returns list of products"""
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

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
