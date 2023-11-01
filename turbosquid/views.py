from django.contrib.auth.views import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from accounts.permission import IsAdminPermission
from .models import Category, Product
from .serializer import CategorySerializer, ProductSerializer

User = get_user_model()


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category = Category.objects.all().order_by('-created_at')
        category_serializer = CategorySerializer(category, many=True)
        return Response(category_serializer.data)


class AddCategoryAPIView(APIView):
    permission_classes = (IsAdminPermission,)

    def post(self, request):
        request.data._mutable = True
        data = request.data
        data['user_id'] = request.user.id
        product_serializer = ProductSerializer(data=data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


# class UpdateDestroyAPIView(APIView):
#     permission_classes = (IsAdminPermission,)
#
#     def put(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#
#             product.save()
#         except Exception as e:
#             return Response({"success": False, "message": e}, status=400)
#         return Response({"success": True})
#
#     def patch(self, request):
#         pass
#
#     def delete(self, request, pk):
#         Product.objects.get(pk=pk).delete()
#         return Response(status=204)


class UpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = []
    permission_classes = (IsAdminPermission,)

