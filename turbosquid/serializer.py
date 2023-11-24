from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from .documents import ProductDocument
from .models import Category, Product, Subscriber, ShoppingCart
from .tasks import sent_email


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer

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


class QuerySerializer(Serializer):
    q = CharField(required=False)


class BlogDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ProductDocument

        fields = (
            'title',
            'description'
        )

