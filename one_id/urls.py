from django.urls import path
from .views import OneIDAuthAPIView

urlpatterns = [
    path('code', OneIDAuthAPIView.as_view(), name='one_code'),
]
