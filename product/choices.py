from django.db import models

class PlantSizeChoices(models.TextChoices):
    SMALL = 'Small', 'Small'
    MEDIUM = 'Medium', 'Medium'
    LARGE = 'Large', 'Large'