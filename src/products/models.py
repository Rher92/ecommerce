from django.db import models

from utils.models import BaseCreatedUpdatedModel


class Product(BaseCreatedUpdatedModel):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    price = models.FloatField(
        null=False,
        blank=False,
        default=0.0     
    )
    stock = models.IntegerField(
        null=False,
        blank=False,
        default=0        
    )

    def __str__(self):
        return f'{self.name}'
