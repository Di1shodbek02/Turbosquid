from django.contrib.auth.views import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permission import IsAdminPermission
from .models import Product, Category, ShoppingCart, Comment
from .serializer import ProductSerializer, ProductSerializerForPost, SubscriberSerializer, CategorySerializer, \
    AddToCartSerializer, CommentSerializer

User = get_user_model()


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return Response(category_serializer.data)


class ProductAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(product_serializer.data)


class AddProductAPIView(GenericAPIView):
    permission_classes = (IsAdminPermission,)
    serializer_class = ProductSerializerForPost

    def post(self, request, format=None): # noqa
        mutable_data = request.data.copy()
        mutable_data['user_id'] = request.user.id
        product_serializer = ProductSerializerForPost(data=mutable_data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class AddCategoryAPIView(GenericAPIView):
    permission_classes = (IsAdminPermission,)
    serializer_class = CategorySerializer

    def post(self, request):

        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
        return Response(category_serializer.data)


class UpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminPermission,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForPost

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SubscriberAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SubscriberSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AddToCartAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def post(self, request):
        count = request.POST.get('count')
        user_id = request.user.id
        product_id = request.POST.get('product_id')

        try:
            user = User.objects.get(pk=user_id)
            product = Product.objects.get(pk=product_id)
            cart_product = ShoppingCart.objects.filter(user=user, product=product)

            if not cart_product:
                cart_product = ShoppingCart.objects.create(
                    count=count,
                    user=user,
                    product=product,
                )
                cart_product.save()

            else:
                return Response({'success': False, 'message': 'This product already exists your cart'})

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response({'success': True, 'message': 'Successfully added!'}, status=200)


class AddCommentAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = self.kwargs.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'success': False, 'message': 'Product not found'}, status=404)

        request.data['user'] = user.id
        request.data['product'] = product.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

        return Response({'success': True, 'message': 'Successfully added comment!', 'data': serializer.data}, status=201)


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


# class ProductLikeAPIView(GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProductLikeSerializer
#
#     def post(self, request):
#         user_id = request.POST.get('user_id')
#         product_id = request.POST.get('product_id')
#
#         try:
#             like = ProductLike.objects.create(
#                 user_id=user_id,
#                 product_id=product_id
#             )
#
#             product = Product.objects.get(id=product_id)
#             if like.is_like:
#                 product.likes += 1
#             else:
#                 product.likes -= 1
#
#             like.save()
#             product.save()
#
#         except Exception as e:
#             return Response({'success': False, 'message': str(e)}, status=400)
#
#         return Response({'success': True, 'message': 'Successfully added like/dislike'})





