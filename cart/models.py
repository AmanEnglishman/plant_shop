from django.db import models

from greenshop.settings import AUTH_USER_MODEL
from product.models import Plant


class Cart(models.Model):
    user = models.OneToOneField(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.user.email}'

    @property
    def cart_total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        verbose_name='Растение'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'plant')

    def __str__(self):
        return f'{self.quantity} / {self.plant.name}'

    @property
    def total_price(self):
        return self.plant.final_product_price() * self.quantity
