from django.urls import path

from orders import views


urlpatterns = [
    path("", views.OrderListCreateView.as_view(), name="order"),
    path("<int:id>/", views.OrderUpdateDeleteView.as_view(), name="order_detail"),
    path("<int:order_id>/items/", views.OrderItemListCreateView.as_view(), name="order_item"),
    path("<int:order_id>/items/<int:order_item_id>/", views.OrderItemDetailView.as_view(), name="order_item_detail"),
]
