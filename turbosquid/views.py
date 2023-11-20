from django.contrib.auth.views import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permission import IsAdminPermission
from .models import Product, Category, ShoppingCart, Comment, ProductLike
from .serializer import ProductSerializer, ProductSerializerForPost, SubscriberSerializer, CategorySerializer, \
    AddToCartSerializer, ProductLikeSerializer

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
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)


class AddProductAPIView(GenericAPIView):
    permission_classes = (IsAdminPermission,)
    serializer_class = ProductSerializerForPost

    def post(self, request):
        request.data._mutable = True
        data = request.data
        data['user_id'] = request.user.id
        product_serializer = ProductSerializerForPost(data=data)
        if not product_serializer.is_valid(raise_exception=True):
            product_serializer.save()
            return Response({'success': False, 'message': 'This product already exists'}, status=400)
        return Response(product_serializer.data)


class AddCategoryAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def post(self, request):

        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
        return Response(category_serializer.data)


class UpdateDestroyProductAPIView(APIView):
    permission_classes = (IsAdminPermission,)

    def get_object(self, pk):
        return Product.objects.get(pk=pk)

    def put(self, request, pk):
        try:
            product = self.get_object(pk)
            data = ProductSerializerForPost(product, data=request.data)
            data.is_valid(raise_exception=True)
            data.save()
            product.save()
        except Exception as e:
            return Response({"success": False, "message": e}, status=400)
        return Response({"success": True})

    def patch(self, request, pk):
        try:
            product = self.get_object(pk)
            data = ProductSerializerForPost(product, data=request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()
            product.save()
        except Exception as e:
            return Response({"success": False, "message": e}, status=400)
        return Response({"success": True})

    def delete(self, request, pk):
        self.get_object(pk)
        return Response(status=204)


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
    serializer_class = ()

    def post(self, request):
        description = request.POST.get('description')
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')

        try:
            comment = Comment.objects.create(
                description=description,
                user_id=user_id,
                product_id=product_id
            )
            comment.save()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response({'success': True, 'message': 'Successfully added comment!'}, status=200)


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


class ProductLikeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductLikeSerializer

    def post(self, request):
        user = request.POST.get('user_id')
        product = request.POST.get('product_id')
        try:
            like = ProductLike.objects.create(
                user=user,
                product=product
            )
            like.save()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response({'success': True, 'message': 'Successfully added like'})

# class UpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializerForPost
#     permission_classes = (IsAdminPermission,)


# class AddProductAPIView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializerForPost
#     permission_classes = (IsAuthenticated,)


# class AddCategoryAPIView(CreateAPIView):
#     queryset = Category.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = CategorySerializer


# class ProductAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = (IsAuthenticated,)
