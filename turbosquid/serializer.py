from rest_framework.serializers import ModelSerializer

from .models import Category, Product, Subscriber
from .tasks import sent_email


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializerForPost(ModelSerializer):
    def save(self, validated_data):
        product = Product.objects.create(**validated_data)
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            sent_email().delay(subscriber.email, validated_data['title'], validated_data['description'])
            return product

    class Meta:
        model = Product
        fields = "__all__"


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
