from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from orders import serializers


class OrderViewSet(ModelViewSet):
    """ViewSet for orders"""
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderItemViewSet(ModelViewSet):
    """viewSet for order items"""
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = (IsAuthenticated,)
