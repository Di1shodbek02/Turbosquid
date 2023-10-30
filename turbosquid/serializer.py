from rest_framework.serializers import ModelSerializer

from .models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryProductSerializer(ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"
