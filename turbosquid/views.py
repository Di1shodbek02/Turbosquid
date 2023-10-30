from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializer import CategorySerializer


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category = Category.objects.all().order_by('-created_at')
        category_serializer = CategorySerializer(category, many=True)

        return Response(category_serializer.data)


class UpdateDestroyAPIView(APIView):
    permission_classes = ()