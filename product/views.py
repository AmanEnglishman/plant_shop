from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.filters import PlantFilter
from product.models import Plant, Category
from product.paginations import PlantPagination
from product.serializers import PlantSerializer, CategorySerializer


@extend_schema(tags=["GET"], summary="List all plants")
class PlantListAPIView(generics.ListAPIView):  # Список
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


@extend_schema(tags=["GET"], summary="Detail plant")
class PlantDetailAPIView(generics.RetrieveAPIView):  # Детальный просмотр
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = 'id'


class PlantAPIView(APIView):
    def get(self, request):
        plants = Plant.objects.all()
        plant_filter = PlantFilter(request.GET, queryset=plants)
        if plant_filter.is_valid():
            plants = plant_filter.qs
        paginator = PlantPagination()
        paginated_plants = paginator.paginate_queryset(plants, request)
        serializer = PlantSerializer(paginated_plants, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('plants'))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
