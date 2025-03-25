import os
from django.db import models

from account.models import User
from product.choices import PlantSizeChoices
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Тег',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Plant(models.Model):
    sku = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Серийный номер'
    )
    categories = models.ManyToManyField(
        to=Category,
        related_name='plants',
        verbose_name='Категории'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name='Краткое описание'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Цена'
    )
    discount_price = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        default=0.00)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        verbose_name='Рейтинг'
    )
    size = models.CharField(
        max_length=50,
        choices=PlantSizeChoices,
        default=PlantSizeChoices.MEDIUM,
        verbose_name='Размер'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='plants',
        verbose_name='Теги'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Растение'
        verbose_name_plural = 'Растении'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name

    def discount_percentage(self):
        if self.discount_price:
            return (100 * self.discount_price) / self.price

    def final_product_price(self):
        if self.discount_price:
            return self.price - self.discount_price


class PlantImage(models.Model):
    plant = models.ForeignKey(
        to=Plant,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Рисунок'
    )
    image = models.ImageField(
        upload_to='images/plants/',
        verbose_name='Рисунок'
    )

    class Meta:
        verbose_name = 'Рисунок растения'
        verbose_name_plural = 'Рисунки растений'


class PlantComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.plant.name} at {self.created_at}"

    class Meta:
        ordering = ['created_at']


@receiver(post_delete, sender=Plant)
def plant_delete_receiver(sender, instance, **kwargs):
    if hasattr(instance, 'images'):
        for image in instance.images.all():
            if os.path.exists(image.image.path):
                os.remove(image.image.path)
            image.delete()
