from rest_framework import serializers
from product.models import Plant, PlantImage
from .models import Cart, CartItem


class PlantCartImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ('image',)


class PlantCartSerializers(serializers.ModelSerializer):
    images = PlantCartImageSerializers(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ('id', 'name', 'price', 'images', 'discount_price')


class CartItemSerializers(serializers.ModelSerializer):
    plant = PlantCartSerializers(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'plant', 'quantity', 'total')

    def get_total(self, obj):
        return obj.total_price


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)
    cart_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'cart_total_price')

    def get_cart_total_price(self, obj):
        return obj.cart_total_price
