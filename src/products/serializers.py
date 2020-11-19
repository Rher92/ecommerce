from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'price', 'stock']


class ProductToOrderDetails(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'price']

    