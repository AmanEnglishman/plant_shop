from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .models import Cart, CartItem
from product.models import Plant
from .serializers import CartSerializers, CartItemSerializers

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        """Очищает корзину пользователя"""
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Кешируем корзину, чтобы избежать лишнего запроса"""
        if not hasattr(self, 'cart'):
            self.cart = get_object_or_404(Cart, user=self.request.user)
        return CartItem.objects.filter(cart=self.cart)

    def perform_create(self, serializer):
        """Создаёт или обновляет товар в корзине"""
        plant = get_object_or_404(Plant, id=self.request.data.get('plant_id'))
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            plant=plant,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return cart_item

    def create(self, request, *args, **kwargs):
        cart_item = self.perform_create(self.get_serializer())
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Обновление количества товара в корзине"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        quantity = int(quantity)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        else:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
