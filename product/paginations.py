from rest_framework.pagination import PageNumberPagination


class PlantPagination(PageNumberPagination):
    page_size = 9
