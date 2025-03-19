from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.views import APIView

from product.models import Plant
from product.serializers import PlantSerializer


@extend_schema(tags=["GET"], summary="List all plants")
class PlantListAPIView(generics.ListAPIView):  # Список
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantCreateAPIView(generics.CreateAPIView):  # Создать
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


@extend_schema(tags=["PUT"], summary="Update plant")
class PlantUpdateAPIView(generics.UpdateAPIView):  # Обновить
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = 'id'


class PlantDeleteAPIView(generics.DestroyAPIView):  # Удалить
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = 'id'


@extend_schema(tags=["GET"], summary="Detail plant")
class PlantDetailAPIView(generics.RetrieveAPIView):  # Детальный просмотр
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = 'id'


class PlantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
