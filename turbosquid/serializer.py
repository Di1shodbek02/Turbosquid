from rest_framework.serializers import ModelSerializer

from .models import Category, Product, Subscriber
from .tasks import sent_email


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['parent']


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializerForPost(ModelSerializer):
    def create(self, **validated_data):
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            sent_email.delay(subscriber.email, validated_data['title'], validated_data['price'])
        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        exclude = ['parent']


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
