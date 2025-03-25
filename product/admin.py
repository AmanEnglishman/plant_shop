from django.contrib import admin
from .models import Plant, Category, Tag, PlantImage, PlantComment


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class PlantCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class PlantTagAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantComment)
class PlantCommentAdmin(admin.ModelAdmin):
    pass
