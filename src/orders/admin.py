from django.contrib import admin

from .models import Order, OrderDetail

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass