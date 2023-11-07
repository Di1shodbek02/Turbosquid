from django.urls import path
from .views import OneIDAuthAPIView, OneIDCodeAPIVIEW

urlpatterns = [
    path('login', OneIDAuthAPIView.as_view(), name='one_login'),
    path('code', OneIDCodeAPIVIEW.as_view(), name='one_code'),
]
