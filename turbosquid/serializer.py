from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Category, Product, Subscriber, ShoppingCart
from .tasks import sent_email


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    # category = CategorySerializer

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerForPost(ModelSerializer):
    def create(self, validated_data):
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            sent_email.delay(subscriber.email, validated_data['title'], validated_data['price'])
        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = '__all__'


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class AddToCartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        return ShoppingCart.objects.create(user=user, **validated_data)


class QuerySerializer(Serializer):
    q = CharField(required=False)


class CartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ('user',)
