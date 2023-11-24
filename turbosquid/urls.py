from django.urls import path
from .views import ProductAPIView, SubscriberAPIView, AddCategoryAPIView, \
    UpdateDestroyProductAPIView, SearchAPIView, CategoryGenericAPIView, AddToCartGenericAPIView, \
    ProductListGenericAPIView, UpdateDestroyCartGenericAPIView, AddProductAPIView, CartGenericAPIView

urlpatterns = [
    path('category-list', CategoryGenericAPIView.as_view(), name='category_list'),
    path('add-to-cart', AddToCartGenericAPIView.as_view(), name='add-to-cart'),
    path('products-list', ProductAPIView.as_view(), name='products_list'),
    path('create-category', AddCategoryAPIView.as_view(), name="create_category"),
    path('create-product', AddProductAPIView.as_view(), name="create_product"),
    path('subscriber', SubscriberAPIView.as_view(), name="subscriber"),
    path('update-product/<int:pk>', UpdateDestroyProductAPIView.as_view(), name='update_product'),
    path('search', SearchAPIView.as_view(), name='search'),
    path('category-product/<int:category_id>', ProductListGenericAPIView.as_view(), name='category_product'),
    path('update-cart/<int:pk>', UpdateDestroyCartGenericAPIView.as_view(), name='update_cart'),
    path('cart', CartGenericAPIView.as_view(), name='cart'),
]
