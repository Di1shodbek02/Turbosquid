from django.urls import path

from .views import ProductAPIView, AddProductAPIView, UpdateDestroyAPIView, SubscriberAPIView

urlpatterns = [
    path('products-list', ProductAPIView.as_view(), name='products_list'),
    path('create-product', AddProductAPIView.as_view(), name="create_product"),
    path('product/<int:pk>', UpdateDestroyAPIView.as_view(), name="product"),
    path('subscriber', SubscriberAPIView.as_view(), name="subscriber")
]
