from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from product.filters import PlantFilter
from product.models import Plant, Category
from product.paginations import PlantPagination
from product.serializers import PlantSerializer, CategorySerializer, PlantDetailSerializer, PlantCommentsSerializer


@extend_schema(tags=["GET"], summary="List all plants")
class PlantListAPIView(generics.ListAPIView):  # Список
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


@extend_schema(tags=["GET"], summary="Detail plant")
class PlantDetailAPIView(APIView):  # Детальный просмотр
    def get(self, request, plant_id):
        plant = get_object_or_404(Plant.objects.prefetch_related('images', 'categories', 'tags', 'comments'),
                                  id=plant_id)
        similar_plants = Plant.objects.filter(
            categories__in=plant.categories.all()
        ).exclude(id=plant.id).distinct()
        if not plant.tags.exists():
            similar_plants = similar_plants.annotate(
                tag_match_count=Count(
                    'tags',
                    filter=Q(tags__in=plant.tags.all).order_by('-tag_match_count')))
        similar_plants = similar_plants[0:5]
        plant_serializer = PlantDetailSerializer(plant)
        similar_serializer = PlantSerializer(similar_plants, many=True)

        return Response({
            'plant': plant_serializer.data,
            'similar_plants': similar_serializer.data,
        })


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


class PlantCommentCreateAPIView(APIView):
    def post(self, request, plant_id):
        plant = get_object_or_404(Plant, id=plant_id)
        data = request.data.copy()
        data['plant'] = plant.id

        print(f"Plant ID: {data['plant']}")

        # if request.user.is_authenticated:
        #     data['user'] = request.user.id
        # else:
        #     return Response({'detail': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PlantCommentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
