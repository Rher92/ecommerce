from rest_framework import serializers

from products.models import Product
from products.serializers import ProductToOrderDetails
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductToOrderDetails(read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['pk', 'order_detail','pesos_total', 'usd_total']


class OrderUpdateSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['pk', 'order_detail','pesos_total', 'usd_total']

    def validate(self, data):
        payload = self.initial_data
        if (not payload or len(payload) < 2):
            raise serializers.ValidationError({"detail": "all necessary parameters were not sent."})

        product_pk = payload.get('product')
        try:
            product_quantity = int(payload.get('quantity'))
        except:
            raise serializers.ValidationError({"detail": "product_quantity is not a integer"})

        if product_quantity < 1:
            raise serializers.ValidationError({"detail": "the quantity is zero"})
            

        product = Product.objects.filter(pk=product_pk).first()
        if not product:
            raise serializers.ValidationError({"detail": f"product with id:{product_pk} does not exist"})

        _order_detail = self.instance.order_detail.filter(product__pk=product_pk).first()
        if _order_detail:
            temporal_stock = product.stock
            temporal_got = _order_detail.quantity
            temporal_stock += temporal_got

            if temporal_stock < product_quantity:
                raise serializers.ValidationError({"detail": f"the stock of the {product.name} does not get the requirement"})
        else:
            if product.stock < product_quantity:
                raise serializers.ValidationError({"detail": f"the stock of the {product.name} does not get the requirement"})

        return data  

    def update(self, instance, params):
        product_pk = self.initial_data.get('product')
        product_quantity = int(self.initial_data.get('quantity'))
        _order_detail = instance.order_detail.filter(product__pk=product_pk).first()
        product = Product.objects.filter(pk=product_pk).first()
        
        if _order_detail:
            temporal_stock = product.stock
            temporal_got = _order_detail.quantity
            temporal_stock += temporal_got
            product.stock = temporal_stock-product_quantity
            _order_detail.quantity = product_quantity
            _order_detail.save()
            product.save()
        else:
            product.stock = product.stock-product_quantity
            product.save()
            
            _order_detail = OrderDetail(
                product=product,
                quantity=product_quantity,
                order=instance
            )
            _order_detail.save()

        return _order_detail.order