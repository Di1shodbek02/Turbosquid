from django.urls import path

from .views import CategoryAPIView, UpdateDestroyAPIView

urlpatterns = [
    path('category', CategoryAPIView.as_view(), name="category"),
    path('product/<int:pk>', UpdateDestroyAPIView.as_view(), name="product"),
]
