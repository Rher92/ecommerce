from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from utils.models import BaseCreatedUpdatedModel
from products.models import Product
from .fetches import get_dollar_blue

class Order(BaseCreatedUpdatedModel):
    pass

    def __str__(self):
        return f'{self.pk}'

    @property
    def pesos_total(self):
        total = 0
        for item in self.order_detail.all():
            _total = item.quantity * item.product.price
            total = total + _total
        return total        

    @property
    def usd_total(self):
        pesos_total = self.pesos_total
        dollar_total = 0
        if pesos_total != 0:
            quotation = get_dollar_blue()
            dollar_total = quotation * pesos_total
        return dollar_total

    

class OrderDetail(BaseCreatedUpdatedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_detail',
        related_query_name='order_detail'
    )
    quantity = models.IntegerField()
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_detail',
        related_query_name='order_detail'
    )

    def __str__(self):
        return f'order:{self.order} - {self.product}'
