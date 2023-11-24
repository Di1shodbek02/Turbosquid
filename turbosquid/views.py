from django.contrib.auth.views import get_user_model

from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, ShoppingCart
from .serializer import ProductSerializer, ProductSerializerForPost, SubscriberSerializer, CategorySerializer, \
    AddToCartSerializer, QuerySerializer, CartSerializer

User = get_user_model()


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return Response(category_serializer.data)


class CategoryGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get(self, request):
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True, context={'request': request})
        return Response(category_serializer.data)


class ProductListGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        serializer_product = self.get_serializer(products, many=True)
        return Response(serializer_product.data)


class ProductAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(product_serializer.data)


class AddProductAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializerForPost

    def post(self, request, format=None):  # noqa
        mutable_data = request.data.copy()
        mutable_data['user_id'] = request.user.id
        product_serializer = ProductSerializerForPost(data=mutable_data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class AddCategoryAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def post(self, request):
        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
        return Response(category_serializer.data)


class UpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForPost


class SubscriberAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SubscriberSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AddToCartGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def post(self, request):
        serializer_cart = self.get_serializer(data=request.data)
        serializer_cart.is_valid(raise_exception=True)
        serializer_cart.save()
        return Response(serializer_cart.data)

    # def get_serializer(self, instance, *args, **kwargs):
    #     kwargs['context'] = self.get_serializer_context()
    #     return AddToCartSerializer(instance, *args, **kwargs)



class UpdateDestroyCartGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def delete(self, request, pk):
        cart_product = ShoppingCart.objects.get(pk=pk)

        try:
            cart_product.delete()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response(status=204)


class UpdateDestroyCartAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def get_object(self, pk):  # noqa
        return ShoppingCart.objects.get(pk=pk)

    def delete(self, request, pk):
        cart_product = self.get_object(pk)

        try:
            cart_product.delete()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response({'success': True, 'message': 'Delete product'}, status=200)


class SearchAPIView(GenericAPIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)  # noqa
    def get(self, request):
        query = request.query_params.get('q', '')
        search = Search(index='turbosquid').query('multi_match', query=query, fields=('title', 'description'))
        results = [hit.to_dict() for hit in search.execute()]
        return Response(results)

# class SearchDocumentViewSet(DocumentViewSet):
#     document = ProductDocument
#     serializer_class = ProductDocument
#
#     filter_backends = [
#         FilteringFilterBackend,
#         SearchFilterBackend,
#         SuggesterFilterBackend,
#         FunctionalSuggesterFilterBackend
#     ]
#
#     search_fields = (
#         'title',
#         'description',
#     )
#
#     filter_fields = {
#         'title': 'title',
#         'description': 'description',
#     }
#
#     suggester_fields = {
#         'title': {
#             'field': 'title.suggest',
#             'suggesters': [
#                 SUGGESTER_COMPLETION,
#             ],
#         }
#     }


class CartGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request):
        cart = ShoppingCart.objects.filter(user=request.user)
        serializer_cart = self.get_serializer(cart, many=True)
        return Response(serializer_cart.data)
