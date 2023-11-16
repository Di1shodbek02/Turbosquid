from django.contrib.auth.views import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permission import IsAdminPermission
from .models import Product
from .serializer import ProductSerializer, ProductSerializerForPost, SubscriberSerializer

User = get_user_model()


# class ProductAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         products = Product.objects.all().order_by('-created_at')
#         product_serializer = ProductSerializer(products, many=True)
#         return Response(product_serializer.data)
#
#
# class AddProductAPIView(APIView):
#     permission_classes = (IsAdminPermission,)
#
#     def post(self, request):
#         request.data._mutable = True
#         data = request.data
#         data['user_id'] = request.user.id
#         product_serializer = ProductSerializerForPost(data=data)
#         product_serializer.is_valid(raise_exception=True)
#         product_serializer.save()
#         return Response(product_serializer.data)


# class UpdateDestroyAPIView(APIView):
#     permission_classes = (IsAdminPermission,)
#
#     def get_object(self, pk):
#         return Product.objects.get(pk=pk)
#
#     def put(self, request, pk):
#         try:
#             product = self.get_object(pk)
#             data = ProductSerializerForPost(product, data=request.data)
#             data.is_valid(raise_exception=True)
#             data.save()
#             product.save()
#         except Exception as e:
#             return Response({"success": False, "message": e}, status=400)
#         return Response({"success": True})
#
#     def patch(self, request, pk):
#         try:
#             product = self.get_object(pk)
#             data = ProductSerializerForPost(product, data=request.data, partial=True)
#             data.is_valid(raise_exception=True)
#             data.save()
#             product.save()
#         except Exception as e:
#             return Response({"success": False, "message": e}, status=400)
#         return Response({"success": True})
#
#     def delete(self, request, pk):
#         self.get_object(pk)
#         return Response(status=204)

class UpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForPost
    permission_classes = (IsAdminPermission,)


class AddProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForPost
    permission_classes = (IsAdminPermission,)


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class SubscriberAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SubscriberSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
