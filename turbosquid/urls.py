from django.urls import path

from .views import ProductAPIView, AddProductAPIView, SubscriberAPIView, AddCategoryAPIView, \
    AddToCartAPIView, AddCommentAPIView, UpdateDestroyProductAPIView

urlpatterns = [
    path('add-cart', AddToCartAPIView.as_view(), name='add_cart'),
    path('products-list', ProductAPIView.as_view(), name='products_list'),
    path('create-product', AddProductAPIView.as_view(), name="create_product"),
    path('create-category', AddCategoryAPIView.as_view(), name="create_category"),
    path('subscriber', SubscriberAPIView.as_view(), name="subscriber"),
    path('add-comments', AddCommentAPIView.as_view(), name='add_comments'),
    path('update-product/<int:pk>', UpdateDestroyProductAPIView.as_view(), name='update_product'),
]
