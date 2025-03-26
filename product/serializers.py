from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from product.models import Plant, Category, PlantImage, Tag, PlantComment


class PlantImageSerializer(ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ('id', 'image')


class PlantSerializer(ModelSerializer):
    images = PlantImageSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    final_product_price = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = ('id', 'name', 'price', 'images', 'final_product_price', 'discount_percentage')

    def get_discount_percentage(self, obj):
        return obj.discount_percentage()

    def get_final_product_price(self, obj):
        return obj.final_product_price()


class CategorySerializer(ModelSerializer):
    product_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count')


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PlantCommentSerializer(ModelSerializer):
    class Meta:
        model = PlantComment
        fields = ('id', 'plant', 'text', 'created_at',)
        read_only_fields = ('id', 'created_at')


class PlantDetailSerializer(ModelSerializer):
    images = PlantImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    comments = PlantCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = (
            'id', 'sku', 'category', 'tags', 'images', 'short_description', 'description', 'price', 'rating', 'size',
            'comments'
        )
