from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import get_user_model
from .models import Category
from .serializer import CategorySerializer, ProductSerializer

User = get_user_model()


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category = Category.objects.all().order_by('-created_at')
        category_serializer = CategorySerializer(category, many=True)
        return Response(category_serializer.data)

    def post(self, request):
        request.data._mutable = True
        data = request.data
        data['user_id'] = request.user.id
        product_serializer = ProductSerializer(data=data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)
