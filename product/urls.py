from django.urls import path

from .views import *

urlpatterns = [
    path('', PlantAPIView.as_view(), name='plant_list'),
    path('<int:plant_id>/', PlantDetailAPIView.as_view(), name='plant_detail'),
    path('category/', CategoryAPIView.as_view(), name='category-list'),
    path('comments/', PlantCommentCreateAPIView.as_view(), name='plant_comment_create'),
    path('comments/delete/<id>/', PlantCommentCreateAPIView.as_view(), name='plant_comment_create'),

]
